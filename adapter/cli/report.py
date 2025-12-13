from rich.console import Console
from rich.table import Table

from domain.goose import FlockGoose, HonkGoose, WarGoose
from repository.stats import (
    Statistic,
    _goose_key,
    _iter_all_individual_geese,
    _player_key,
)
from usecase.interface import GooseCollection, PlayerCollection


def _calc_success_rate(success: int, fail: int) -> str:
    total = success + fail
    if total == 0:
        return '0%'
    return f'{success * 100 // total}%'


def print_statistic_report(  # noqa: PLR0915
    stat: Statistic,
    *,
    players: PlayerCollection,
    geese: GooseCollection,
    casino_bank: int,
) -> None:
    """Выводит красивый отчет по статистике в консоль"""
    console = Console()

    war_total = 0
    honk_total = 0
    for g in geese:
        if isinstance(g, WarGoose):
            war_total += 1
        elif isinstance(g, HonkGoose):
            honk_total += 1
        elif isinstance(g, FlockGoose):
            war_total += len(g.war)
            honk_total += len(g.honk)

    # Общая статистика
    summary_table = Table(
        title='Общая статистика', show_header=True, header_style='bold magenta'
    )
    summary_table.add_column('Метрика', style='cyan', justify='left')
    summary_table.add_column('Значение', style='green', justify='right')

    summary_table.add_row('Игроков', str(len(players)))
    summary_table.add_row('Гусей атакующих', str(war_total))
    summary_table.add_row('Гусей кричащих', str(honk_total))
    summary_table.add_row('Стай создано', str(stat.flocks_created))

    console.print(summary_table)

    # Банк казино
    bank_table = Table(
        title='Банк казино', show_header=True, header_style='bold magenta'
    )
    bank_table.add_column('Параметр', style='cyan')
    bank_table.add_column('Значение', style='yellow', justify='right')

    bank_delta = casino_bank - stat.casino_bank_start
    bank_delta_str = (
        f'[green]+{bank_delta}[/green]'
        if bank_delta >= 0
        else f'[red]{bank_delta}[/red]'
    )

    bank_table.add_row('Начальный', str(stat.casino_bank_start))
    bank_table.add_row('Текущий', str(casino_bank))
    bank_table.add_row('Изменение', bank_delta_str)

    console.print(bank_table)

    # Частота событий
    if stat.event_counts:
        event_table = Table(
            title='Частота событий', show_header=True, header_style='bold magenta'
        )
        event_table.add_column('Событие', style='cyan')
        event_table.add_column('Количество', style='green', justify='right')

        for name in sorted(stat.event_counts):
            event_table.add_row(name, str(stat.event_counts[name]))

        console.print(event_table)

    # Статистика атак
    attack_table = Table(
        title='Статистика атак', show_header=True, header_style='bold magenta'
    )
    attack_table.add_column('Тип атаки', style='cyan')
    attack_table.add_column('Успешные', style='green', justify='right')
    attack_table.add_column('Провальные', style='red', justify='right')
    attack_table.add_column('Всего', style='yellow', justify='right')
    attack_table.add_column('Успешность', style='blue', justify='right')

    attack_table.add_row(
        'War Goose',
        str(stat.war_attack_success),
        str(stat.war_attack_fail),
        str(stat.war_attack_success + stat.war_attack_fail),
        _calc_success_rate(stat.war_attack_success, stat.war_attack_fail),
    )
    attack_table.add_row(
        'Honk Goose',
        str(stat.honk_attack_success),
        str(stat.honk_attack_fail),
        str(stat.honk_attack_success + stat.honk_attack_fail),
        _calc_success_rate(stat.honk_attack_success, stat.honk_attack_fail),
    )
    attack_table.add_row(
        'Flock Goose',
        str(stat.flock_attack_success),
        str(stat.flock_attack_fail),
        str(stat.flock_attack_success + stat.flock_attack_fail),
        _calc_success_rate(stat.flock_attack_success, stat.flock_attack_fail),
    )

    console.print(attack_table)

    # Баланс игроков
    player_table = Table(
        title='Баланс игроков', show_header=True, header_style='bold magenta'
    )
    player_table.add_column('Игрок', style='cyan')
    player_table.add_column('Начальный', style='yellow', justify='right')
    player_table.add_column('Текущий', style='yellow', justify='right')
    player_table.add_column('Изменение', justify='right')

    for p in sorted(players, key=lambda x: x.name):
        start = stat.player_start_balance.get(_player_key(p), p.balance)
        delta = p.balance - start
        delta_str = f'[green]+{delta}[/green]' if delta >= 0 else f'[red]{delta}[/red]'

        player_table.add_row(p.name, str(start), str(p.balance), delta_str)

    console.print(player_table)

    # Баланс гусей (только с изменениями)
    goose_changes = []
    for g in _iter_all_individual_geese(geese):
        start = stat.goose_start_balance.get(_goose_key(g), g.balance)
        delta = g.balance - start
        if delta != 0:
            goose_changes.append((g.name, start, g.balance, delta))

    if goose_changes:
        goose_table = Table(
            title='Баланс гусей (с изменениями)',
            show_header=True,
            header_style='bold magenta',
        )
        goose_table.add_column('Гусь', style='cyan')
        goose_table.add_column('Начальный', style='yellow', justify='right')
        goose_table.add_column('Текущий', style='yellow', justify='right')
        goose_table.add_column('Изменение', justify='right')

        for name, start, current, delta in sorted(goose_changes, key=lambda x: x[0]):
            delta_str = (
                f'[green]+{delta}[/green]' if delta >= 0 else f'[red]{delta}[/red]'
            )
            goose_table.add_row(name, str(start), str(current), delta_str)

        console.print(goose_table)

    # Статистика станов
    stun_table = Table(
        title='Статистика станов', show_header=True, header_style='bold magenta'
    )
    stun_table.add_column('Тип', style='cyan')
    stun_table.add_column('Дней в стане', style='red', justify='right')

    stun_table.add_row('Игроки', str(stat.player_stun_days))
    stun_table.add_row('Гуси', str(stat.goose_stun_days))

    console.print(stun_table)
