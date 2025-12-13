from dataclasses import dataclass, field

from domain.effect import Effect, StunEffect
from domain.engine import EffectEngine
from domain.goose import FlockGoose, Goose, HonkGoose, WarGoose
from domain.player import Player
from usecase.interface import CasinoStatistic, GooseCollection, PlayerCollection


def _player_key(p: Player) -> str:
    return f'player:{p.name}'


def _goose_key(g: Goose) -> str:
    return f'goose:{g.name}'


def _iter_all_individual_geese(geese: GooseCollection) -> list[WarGoose | HonkGoose]:
    out: list[WarGoose | HonkGoose] = []
    for g in geese:
        if isinstance(g, (WarGoose, HonkGoose)):
            out.append(g)
            continue
        if isinstance(g, FlockGoose):
            out.extend(g.war)
            out.extend(g.honk)
            continue
    return out


@dataclass(slots=True)
class Statistic(CasinoStatistic):
    event_counts: dict[str, int] = field(default_factory=dict)

    war_attack_success: int = 0
    war_attack_fail: int = 0

    honk_attack_success: int = 0
    honk_attack_fail: int = 0

    flock_attack_success: int = 0
    flock_attack_fail: int = 0

    flocks_created: int = 0

    player_stun_days: int = 0
    goose_stun_days: int = 0

    player_start_balance: dict[str, int] = field(default_factory=dict)
    goose_start_balance: dict[str, int] = field(default_factory=dict)

    casino_bank_start: int = 0

    def on_init(
        self,
        *,
        players: PlayerCollection,
        geese: GooseCollection,
        casino_bank: int,
    ) -> None:
        if self.casino_bank_start == 0:
            self.casino_bank_start = casino_bank

        for p in players:
            key = _player_key(p)
            if key not in self.player_start_balance:
                self.player_start_balance[key] = p.balance

        for g in _iter_all_individual_geese(geese):
            key = _goose_key(g)
            if key not in self.goose_start_balance:
                self.goose_start_balance[key] = g.balance

    def on_step_begin(
        self,
        *,
        step: int,
        players: PlayerCollection,
        geese: GooseCollection,
        effects: EffectEngine,
        casino_bank: int,
    ) -> None:
        for p in players:
            if effects.check_effect(p, StunEffect):
                self.player_stun_days += 1

        for g in geese:
            if effects.check_effect(g, StunEffect):
                self.goose_stun_days += 1

    def on_event_selected(self, *, step: int, event_name: str) -> None:
        self.event_counts[event_name] = self.event_counts.get(event_name, 0) + 1

    def on_bet(
        self,
        *,
        step: int,
        player: Player,
        bet: int,
        win: bool,
        multiplier: int,
        payout: int,
        casino_bank: int,
    ) -> None:
        return

    def on_attack(
        self,
        *,
        step: int,
        goose: Goose,
        attacked_self: bool,
    ) -> None:
        if isinstance(goose, FlockGoose):
            if attacked_self:
                self.flock_attack_fail += 1
            else:
                self.flock_attack_success += 1
            return

        if isinstance(goose, WarGoose):
            if attacked_self:
                self.war_attack_fail += 1
            else:
                self.war_attack_success += 1
            return

        if isinstance(goose, HonkGoose):
            if attacked_self:
                self.honk_attack_fail += 1
            else:
                self.honk_attack_success += 1
            return

    def on_flock_create(self, *, step: int, size: int) -> None:
        self.flocks_created += 1

    def on_tick_end(
        self,
        *,
        step: int,
        effects: list[Effect],
        casino_bank: int,
    ) -> None:
        return
