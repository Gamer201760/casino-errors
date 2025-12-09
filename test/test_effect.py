import pytest

from domain.effect import OnceStealBalance, StunEffect
from domain.goose import HonkGoose, WarGoose
from domain.player import Player


@pytest.mark.parametrize(
    (
        'start_balance',
        'delta',
        'expected_balance_after_first_tick',
        'expected_balance_after_second_tick',
    ),
    [
        # обычная кража
        (100, -30, 70, 70),
        # кража в минус
        (10, -50, -40, -40),
        # пополнение
        (0, 10, 10, 10),
    ],
)
def test_once_steal_balance_ticks(
    start_balance: int,
    delta: int,
    expected_balance_after_first_tick: int,
    expected_balance_after_second_tick: int,
) -> None:
    # arrange
    player = Player(name='p', balance=start_balance)
    goose = WarGoose(name='war', strength=10)
    effect = OnceStealBalance(source=goose, target=player, delta=delta)

    # act
    effect.on_tick()

    # assert
    assert player.balance == expected_balance_after_first_tick
    assert effect.duration == 0

    # act
    effect.on_tick()

    # assert
    assert player.balance == expected_balance_after_second_tick
    assert effect.duration == -1


@pytest.mark.parametrize(
    (
        'duration_start',
        'expected_duration_after_first_tick',
        'expected_duration_after_second_tick',
    ),
    [
        # один тик
        (1, 0, -1),
        # несколько тиков
        (3, 2, 1),
        # нулевой стан
        (0, -1, -2),
    ],
)
def test_stun_effect_ticks(
    duration_start: int,
    expected_duration_after_first_tick: int,
    expected_duration_after_second_tick: int,
) -> None:
    goose = HonkGoose(name='h', honk_volume=10)
    player = Player(name='p')
    effect = StunEffect(source=goose, target=player, duration=duration_start)
    before_balance = player.balance  # контроль побочных эффектов

    effect.on_tick()

    assert effect.duration == expected_duration_after_first_tick
    # стан не трогает баланс только ход
    assert player.balance == before_balance

    effect.on_tick()

    assert effect.duration == expected_duration_after_second_tick
    assert player.balance == before_balance
