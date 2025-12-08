import pytest

from domain.effect import OnceStealBalance, StunEffect
from domain.goose import HonkGoose, WarGoose
from domain.player import Player


@pytest.mark.parametrize(
    'player_balance, strength, expected_steal',
    [
        (100, 30, 30),
        (10, 30, 10),
        (0, 30, 0),
    ],
)
def test_wargoose_act_player_steal(player_balance, strength, expected_steal):
    player = Player(name='p', balance=player_balance)
    goose = WarGoose(name='war', strength=strength, lucky=0, balance=0)

    effects = goose.act_player(player)

    assert len(effects) == 2
    assert isinstance(effects[0], OnceStealBalance)
    assert isinstance(effects[1], OnceStealBalance)

    # Первый эффект: игрок теряет деньги
    effects[0].on_tick()
    # Второй эффект: гусь получает деньги
    effects[1].on_tick()

    assert player.balance == player_balance - expected_steal
    assert goose.balance == expected_steal


@pytest.mark.parametrize(
    'goose_balance, strength, expected_lost',
    [
        (100, 30, 30),
        (10, 30, 10),
        (0, 30, 0),
    ],
)
def test_wargoose_act_self(goose_balance, strength, expected_lost):
    goose = WarGoose(name='war', strength=strength, lucky=0, balance=goose_balance)

    effects = goose.act_self()

    if expected_lost == 0:
        assert effects == []
    else:
        assert len(effects) == 1
        effect = effects[0]
        assert isinstance(effect, OnceStealBalance)
        effect.on_tick()
        assert goose.balance == goose_balance - expected_lost


@pytest.mark.parametrize(
    'honk_volume, expected_turns',
    [
        (1, 1),
        (5, 1),
        (10, 1),
        (15, 1),
        (20, 2),
        (35, 3),
    ],
)
def test_honk_goose_stun_turns(honk_volume, expected_turns):
    goose = HonkGoose(name='h', honk_volume=honk_volume)
    assert goose._stun_turns() == expected_turns


def test_honk_goose_act_player_creates_stun(player_zero, honk_goose_loud):
    effects = honk_goose_loud.act_player(player_zero)

    assert len(effects) == 1
    effect = effects[0]
    assert isinstance(effect, StunEffect)
    assert effect.source is honk_goose_loud
    assert effect.target is player_zero
    assert effect.duration == honk_goose_loud._stun_turns()


def test_honk_goose_act_self_creates_stun(honk_goose_loud):
    effects = honk_goose_loud.act_self()

    assert len(effects) == 1
    effect = effects[0]
    assert isinstance(effect, StunEffect)
    assert effect.source is honk_goose_loud
    assert effect.target is honk_goose_loud
    assert effect.duration == honk_goose_loud._stun_turns()
