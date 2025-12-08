import pytest

from domain.honk_goose import HonkGoose, StunEffect
from domain.player import Player
from domain.war_goose import OnceStealBalance, WarGoose


@pytest.mark.parametrize(
    'start_balance, delta, expected_after_first, expected_after_second',
    [
        (100, -30, 70, 70),
        (10, -50, -40, -40),
        (0, 10, 10, 10),
    ],
)
def test_once_steal_balance_ticks(
    start_balance, delta, expected_after_first, expected_after_second
):
    player = Player(name='p', balance=start_balance)
    goose = WarGoose(name='war', strength=10)
    effect = OnceStealBalance(source=goose, target=player, delta=delta)

    effect.on_tick()
    assert player.balance == expected_after_first
    assert effect.duration == 0

    effect.on_tick()
    assert player.balance == expected_after_second
    assert effect.duration == -1


@pytest.mark.parametrize(
    'duration_start, expected_after_first, expected_after_second',
    [
        (1, 0, -1),
        (3, 2, 1),
    ],
)
def test_stun_effect_ticks(duration_start, expected_after_first, expected_after_second):
    goose = HonkGoose(name='h', honk_volume=10)
    player = Player(name='p')
    effect = StunEffect(source=goose, target=player, duration=duration_start)

    effect.on_tick()
    assert effect.duration == expected_after_first

    effect.on_tick()
    assert effect.duration == expected_after_second
