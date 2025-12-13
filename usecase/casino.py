import logging
import random
from typing import Callable

from domain.chip import Chip
from domain.config import CasinoConfig
from domain.effect import Effect, OnceStealBalance, StunEffect
from domain.engine import EffectEngine
from domain.entity import Entity
from domain.goose import FlockGoose, Goose, HonkGoose, WarGoose
from domain.player import Player
from usecase.interface import (
    CasinoBalance,
    CasinoStatistic,
    GooseCollection,
    PlayerCollection,
)

logger = logging.getLogger(__name__)

CASINO_BANK_KEY = 'casino:bank'


def clamp01(x: float) -> float:
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


class Casino:
    def __init__(
        self,
        players: PlayerCollection,
        geese: GooseCollection,
        balances: CasinoBalance,
        *,
        stat: CasinoStatistic,
        config: CasinoConfig | None = None,
        balance: int = 0,
        effects: EffectEngine | None = None,
    ) -> None:
        self._players = players
        self._geese = geese
        self._balances = balances
        self._stat = stat

        self.balance = balance
        self._config = (config or CasinoConfig()).with_defaults()
        self._rng = random.Random(self._config.seed)

        self._effects = effects or EffectEngine()
        self._step = 0

        self._events: dict[str, Callable] = {
            'bet': self._event_bet,
            'goose_attack': self._event_goose_attack,
            'flock_create': self._event_flock_create,
            'flock_disband': self._event_flock_disband,
            'panic': self._event_panic,
        }

        for p in players:
            self._sync_entity(p)
        for g in geese:
            self._sync_entity(g)

        self._sync_bank()

        self._stat.on_init(
            players=self._players, geese=self._geese, casino_bank=self.balance
        )

    def step(self) -> None:
        self._step += 1
        logger.info(f'шаг {self._step} начало')

        self._stat.on_step_begin(
            step=self._step,
            players=self._players,
            geese=self._geese,
            effects=self._effects,
            casino_bank=self.balance,
        )

        event_name = self._pick_event_name()
        logger.info(f'шаг {self._step} событие {event_name}')

        effects = self._events[event_name]()

        for eff in effects:
            self._effects.add_effect(eff)

        self._effects.tick()

        self._sync_by_effects(effects)
        self._sync_bank()

        self._stat.on_tick_end(
            step=self._step, effects=effects, casino_bank=self.balance
        )

        logger.info(f'шаг {self._step} конец, банк {self.balance}')

    def register_player(self, player: Player) -> None:
        self._players.add(player)
        self._sync_entity(player)
        logger.info(f'игрок {player.name} добавлен')

    def register_goose(self, goose: Goose) -> None:
        self._geese.add(goose)
        self._sync_entity(goose)
        logger.info(f'гусь {goose.name} добавлен')

    def _event_bet(self) -> list[Effect]:
        # игрок под оглушением не может делать ставку
        player = self._pick_player(require_balance=True, require_not_stunned=True)
        if player is None:
            logger.info('ставка пропуск: нет игрока')
            return []

        max_bet = max(
            self._config.bet_min, int(player.balance * self._config.bet_max_fraction)
        )
        bet_value = self._rng.randint(
            self._config.bet_min, min(player.balance, max_bet)
        )
        chip = Chip(bet_value)

        logger.info(f'ставка игрок {player.name} фишка {chip.value}')

        # деньги ставки уходят в банк казино
        player.change_balance(-chip.value)
        self.balance += chip.value

        win_p = self._bet_win_probability(player)
        win = self._rng.random() < win_p

        if not win:
            logger.info(f'результат ставки: проигрыш игрок {player.name}')
            self._sync_entity(player)
            self._stat.on_bet(
                step=self._step,
                player=player,
                bet=chip.value,
                win=False,
                multiplier=0,
                payout=0,
                casino_bank=self.balance,
            )
            return []

        # выплата случайный множитель
        mult = self._rng.randint(1, max(1, self._config.bet_win_multiplier_max))
        payout = chip.value * mult

        # казино платит из банка
        self.balance -= payout
        player.change_balance(payout)

        logger.info(
            f'результат ставки: выигрыш игрок {player.name} множитель {mult} выплата {payout}'
        )
        self._sync_entity(player)

        self._stat.on_bet(
            step=self._step,
            player=player,
            bet=chip.value,
            win=True,
            multiplier=mult,
            payout=payout,
            casino_bank=self.balance,
        )
        return []

    def _event_goose_attack(self) -> list[Effect]:
        # гусь может атаковать игрока или себя в зависимости от удачи
        goose = self._pick_goose()
        player = self._pick_player(require_balance=False, require_not_stunned=False)
        if goose is None or player is None:
            logger.info('атака пропуск: нет цели')
            return []

        p_self = self._self_attack_probability(goose, player)
        self_attack = self._rng.random() < p_self

        self._stat.on_attack(step=self._step, goose=goose, attacked_self=self_attack)

        if self_attack:
            logger.info(f'гусь {goose.name} атаковал сам себя')
            return goose.act_self()

        logger.info(f'гусь {goose.name} атаковал игрока {player.name}')
        return goose.act_player(player)

    def _event_flock_create(self) -> list[Effect]:
        # стая создаётся удалением гусей и добавлением объединённого гуся
        if len(self._geese) < self._config.flock_min_size:
            logger.info('стая пропуск: недостаточно гусей')
            return []

        k_max = min(self._config.flock_max_size, len(self._geese))
        k = self._rng.randint(self._config.flock_min_size, k_max)

        chosen = self._rng.sample(list(self._geese), k)
        for g in chosen:
            self._geese.remove(g)

        flock: Goose = chosen[0]
        for g in chosen[1:]:
            flock = flock + g

        self._geese.add(flock)
        logger.info(f'стая создана размер {k} имя {flock.name}')
        self._stat.on_flock_create(step=self._step, size=k)
        return []

    def _event_flock_disband(self) -> list[Effect]:
        # роспуск удаляет стаю и возвращает исходных гусей
        flocks = [g for g in self._geese if isinstance(g, FlockGoose)]
        if not flocks:
            logger.info('роспуск пропуск: нет стаи')
            return []

        flock = self._rng.choice(flocks)
        self._geese.remove(flock)

        for g in list(flock.geese):
            self._geese.add(g)

        logger.info(f'стая распущена имя {flock.name} размер {flock.count}')
        return []

    def _event_panic(self) -> list[object]:
        # паника заставляет игрока потерять все деньги в пользу банка казино
        player = self._pick_player(require_balance=True, require_not_stunned=False)
        if player is None:
            logger.info('паника пропуск: нет игрока')
            return []

        p = self._panic_probability(player)
        ok = self._rng.random() < p
        if not ok:
            logger.info(f'игрок {player.name} справился с паникой')
            return []

        lost = player.balance
        player.change_balance(-lost)
        self.balance += lost

        logger.info(f'игрок {player.name} запаниковал, потеряно {lost}')
        self._sync_entity(player)
        return []

    def _pick_event_name(self) -> str:
        weights = self._config.event_weights
        names = list(weights.keys())
        ws = [weights[n] for n in names]
        return self._rng.choices(names, weights=ws, k=1)[0]

    def _pick_player(
        self, *, require_balance: bool, require_not_stunned: bool
    ) -> Player | None:
        candidates: list[Player] = []
        for p in self._players:
            if require_balance and p.balance <= 0:
                continue
            if require_not_stunned and self._effects.check_effect(p, StunEffect):
                continue
            candidates.append(p)

        if not candidates:
            return None
        return self._rng.choice(candidates)

    def _pick_goose(self) -> Goose | None:
        if len(self._geese) <= 0:
            return None
        return self._rng.choice(list(self._geese))

    def _bet_win_probability(self, player: Player) -> float:
        p = self._config.bet_win_base + player.lucky * self._config.bet_win_lucky_scale
        return clamp01(p)

    def _panic_probability(self, player: Player) -> float:
        p = self._config.panic_base - player.lucky * self._config.panic_lucky_scale
        return clamp01(p)

    def _self_attack_probability(self, goose: Goose, player: Player) -> float:
        diff = goose.lucky - player.lucky
        p = self._config.self_attack_base - diff * self._config.self_attack_lucky_scale
        return clamp01(p)

    def _sync_by_effects(self, effects: list[object]) -> None:
        for eff in effects:
            if isinstance(eff, OnceStealBalance):
                self._sync_entity(eff.source)
                self._sync_entity(eff.target)

    def _sync_bank(self) -> None:
        self._balances[CASINO_BANK_KEY] = self.balance

    def _sync_entity(self, entity: Entity) -> None:
        if isinstance(entity, Player):
            self._balances[f'player:{entity.name}'] = entity.balance
            return

        if isinstance(entity, (WarGoose, HonkGoose)):
            self._balances[f'goose:{entity.name}'] = entity.balance
            return

        if isinstance(entity, FlockGoose):
            for w in entity.war:
                self._balances[f'goose:{w.name}'] = w.balance
            return
