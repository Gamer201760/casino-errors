from dataclasses import dataclass, field

from rich.console import Console
from rich.table import Table

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

    def report(
        self,
        *,
        players: PlayerCollection,
        geese: GooseCollection,
        casino_bank: int,
    ) -> str:
        console = Console()

        war_total = sum(
            1
            if isinstance(g, WarGoose)
            else len(g.war)
            if isinstance(g, FlockGoose)
            else 0
            for g in geese
        )
        honk_total = sum(
            1
            if isinstance(g, HonkGoose)
            else len(g.honk)
            if isinstance(g, FlockGoose)
            else 0
            for g in geese
        )

        # Общая статистика
        summary_table = Table(title='📊 Общая статистика', header_style='bold magenta')
        summary_table.add_column('Метрика', style='cyan')
        summary_table.add_column('Значение', style='green', justify='right')
        summary_table.add_row('Игроков', str(len(players)))
        summary_table.add_row('Гусей атакующих', str(war_total))
        summary_table.add_row('Гусей кричащих', str(honk_total))
        summary_table.add_row('Стай создано', str(self.flocks_created))
        console.print(summary_table)

        # Банк казино
        bank_table = Table(title='🏦 Банк казино', header_style='bold magenta')
        bank_table.add_column('Параметр', style='cyan')
        bank_table.add_column('Значение', style='yellow', justify='right')
        bank_delta = casino_bank - self.casino_bank_start
        bank_delta_str = (
            f'[green]+{bank_delta}[/green]'
            if bank_delta >= 0
            else f'[red]{bank_delta}[/red]'
        )
        bank_table.add_row('Начальный', str(self.casino_bank_start))
        bank_table.add_row('Текущий', str(casino_bank))
        bank_table.add_row('Изменение', bank_delta_str)
        console.print(bank_table)

        # Частота событий
        if self.event_counts:
            event_table = Table(title='📅 Частота событий', header_style='bold magenta')
            event_table.add_column('Событие', style='cyan')
            event_table.add_column('Количество', style='green', justify='right')
            for name in sorted(self.event_counts):
                event_table.add_row(name, str(self.event_counts[name]))
            console.print(event_table)

        # Статистика атак
        attack_table = Table(title='⚔️ Статистика атак', header_style='bold magenta')
        attack_table.add_column('Тип атаки', style='cyan')
        attack_table.add_column('Успешные', style='green', justify='right')
        attack_table.add_column('Провальные', style='red', justify='right')
        attack_table.add_column('Всего', style='yellow', justify='right')
        attack_table.add_column('Успешность', style='blue', justify='right')

        def _calc_success_rate(success: int, fail: int) -> str:
            total = success + fail
            return '0%' if total == 0 else f'{success * 100 // total}%'

        for goose_type, success, fail in [
            ('War Goose', self.war_attack_success, self.war_attack_fail),
            ('Honk Goose', self.honk_attack_success, self.honk_attack_fail),
            ('Flock Goose', self.flock_attack_success, self.flock_attack_fail),
        ]:
            attack_table.add_row(
                goose_type,
                str(success),
                str(fail),
                str(success + fail),
                _calc_success_rate(success, fail),
            )
        console.print(attack_table)

        # Баланс игроков
        player_table = Table(title='💰 Баланс игроков', header_style='bold magenta')
        player_table.add_column('Игрок', style='cyan')
        player_table.add_column('Начальный', style='yellow', justify='right')
        player_table.add_column('Текущий', style='yellow', justify='right')
        player_table.add_column('Изменение', justify='right')

        for p in sorted(players, key=lambda x: x.name):
            start = self.player_start_balance.get(_player_key(p), p.balance)
            delta = p.balance - start
            delta_str = (
                f'[green]+{delta}[/green]' if delta >= 0 else f'[red]{delta}[/red]'
            )
            player_table.add_row(p.name, str(start), str(p.balance), delta_str)
        console.print(player_table)

        # Баланс гусей (только с изменениями)
        goose_changes = []
        for g in _iter_all_individual_geese(geese):
            start = self.goose_start_balance.get(_goose_key(g), g.balance)
            delta = g.balance - start
            if delta != 0:
                goose_changes.append((g.name, start, g.balance, delta))

        if goose_changes:
            goose_table = Table(title='🦢 Баланс гусей', header_style='bold magenta')
            goose_table.add_column('Гусь', style='cyan')
            goose_table.add_column('Начальный', style='yellow', justify='right')
            goose_table.add_column('Текущий', style='yellow', justify='right')
            goose_table.add_column('Изменение', justify='right')

            for name, start, current, delta in sorted(goose_changes):
                delta_str = (
                    f'[green]+{delta}[/green]' if delta >= 0 else f'[red]{delta}[/red]'
                )
                goose_table.add_row(name, str(start), str(current), delta_str)
            console.print(goose_table)

        # Статистика станов
        stun_table = Table(title='😵 Статистика станов', header_style='bold magenta')
        stun_table.add_column('Тип', style='cyan')
        stun_table.add_column('Дней в стане', style='red', justify='right')
        stun_table.add_row('Игроки', str(self.player_stun_days))
        stun_table.add_row('Гуси', str(self.goose_stun_days))
        console.print(stun_table)

        return ''
