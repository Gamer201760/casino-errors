from collections.abc import Collection

import pytest

from domain.effect import Effect, OnceStealBalance, StunEffect
from domain.goose import FlockGoose, Goose, HonkGoose, WarGoose
from domain.player import Player


def get_stun_effects(effects: Collection[Effect]) -> list[StunEffect]:
    return [e for e in effects if isinstance(e, StunEffect)]


def get_steal_effects(effects: Collection[Effect]) -> list[OnceStealBalance]:
    return [e for e in effects if isinstance(e, OnceStealBalance)]


def test_flock_aggregates_two_geese(
    war1: WarGoose,
    honk1: HonkGoose,
    flock_two: FlockGoose,
) -> None:
    assert flock_two.geese == [war1, honk1]
    assert flock_two.war == [war1]
    assert flock_two.honk == [honk1]

    expected_lucky = int((war1.lucky + honk1.lucky) / 2)
    assert flock_two.lucky == expected_lucky

    expected_honk_volume = int(honk1.honk_volume / 1)
    assert flock_two.honk_volume == expected_honk_volume


def test_flock_aggregates_four_geese(
    flock_four: FlockGoose,
    war1: WarGoose,
    war2: WarGoose,
    honk1: HonkGoose,
    honk2: HonkGoose,
) -> None:
    assert len(flock_four.geese) == 4
    assert war1 in flock_four.geese
    assert war2 in flock_four.geese
    assert honk1 in flock_four.geese
    assert honk2 in flock_four.geese

    assert len(flock_four.war) == 2
    assert war1 in flock_four.war
    assert war2 in flock_four.war

    assert len(flock_four.honk) == 2
    assert honk1 in flock_four.honk
    assert honk2 in flock_four.honk

    expected_lucky = int(
        (war1.lucky + war2.lucky + honk1.lucky + honk2.lucky) / 4,
    )
    assert flock_four.lucky == expected_lucky

    expected_honk_volume = int(
        (honk1.honk_volume + honk2.honk_volume) / 2,
    )
    assert flock_four.honk_volume == expected_honk_volume


def test_flock_act_player_no_balance(
    flock_four: FlockGoose,
    poor_player: Player,
) -> None:
    poor_player.balance = 0

    effects: list[Effect] = flock_four.act_player(poor_player)
    stun_effects = get_stun_effects(effects)
    steal_effects = get_steal_effects(effects)

    assert stun_effects
    assert not any(effect.target is poor_player for effect in steal_effects)


def test_flock_act_self_stuns_all_geese(
    flock_four: FlockGoose,
) -> None:
    effects: list[Effect] = flock_four.act_self()

    stun_effects = get_stun_effects(effects)
    assert len(stun_effects) == len(flock_four.geese) + 1

    expected_turns = max(1, flock_four.honk_volume // 10)
    for effect in stun_effects:
        assert effect.source is flock_four
        assert effect.target in [*flock_four.geese, flock_four]
        assert effect.duration == expected_turns


def test_flock_act_player_with_honk_and_war(
    flock_four: FlockGoose,
    rich_player: Player,
) -> None:
    effects: list[Effect] = flock_four.act_player(rich_player)

    stun_effects = get_stun_effects(effects)
    assert len(stun_effects) == 1
    stun = stun_effects[0]
    assert stun.source is flock_four
    assert stun.target is rich_player

    expected_stun_turns = max(1, flock_four.honk_volume // 10)
    assert stun.duration == expected_stun_turns

    steal_effects = get_steal_effects(effects)
    assert len(steal_effects) == 1 + len(flock_four.war)

    player_steal = next(
        effect for effect in steal_effects if effect.target is rich_player
    )

    total_strength = flock_four.strength
    expected_steal = min(total_strength, rich_player.balance)
    assert player_steal.delta == -expected_steal

    war_deltas = [
        effect.delta for effect in steal_effects if isinstance(effect.target, WarGoose)
    ]
    assert sum(war_deltas) == expected_steal
    assert len(war_deltas) == len(flock_four.war)


def test_flock_act_self_steals_from_each_war(
    flock_four: FlockGoose,
    war1: WarGoose,
    war2: WarGoose,
) -> None:
    war1.balance = 5
    war2.balance = 100

    effects: list[Effect] = flock_four.act_self()

    steal_effects = get_steal_effects(effects)
    assert len(steal_effects) == len(flock_four.war)

    for effect in steal_effects:
        assert effect.source is flock_four
        assert isinstance(effect.target, WarGoose)
        assert effect.target in flock_four.war
        expected_lost = min(effect.target.balance, flock_four.strength)
        assert effect.delta == -expected_lost


def test_flock_add_single_war_updates_aggregates(
    flock_two: FlockGoose,
    war2: WarGoose,
) -> None:
    result = flock_two + war2

    assert result is flock_two
    assert war2 in flock_two.geese
    assert war2 in flock_two.war

    expected_lucky = int(
        sum(goose.lucky for goose in flock_two.geese) / len(flock_two.geese),
    )
    assert flock_two.lucky == expected_lucky


def test_flock_add_single_honk_updates_honk_volume(
    flock_two: FlockGoose,
    honk2: HonkGoose,
) -> None:
    result = flock_two + honk2

    assert result is flock_two
    assert honk2 in flock_two.geese
    assert honk2 in flock_two.honk

    expected_honk_volume = int(
        sum(honk.honk_volume for honk in flock_two.honk) / len(flock_two.honk),
    )
    assert flock_two.honk_volume == expected_honk_volume


def test_flock_merge_two_flocks(
    flock_two: FlockGoose,
    flock_four: FlockGoose,
) -> None:
    result = flock_two + flock_four

    assert result is flock_two
    for goose in flock_four.geese:
        assert goose in flock_two.geese

    assert flock_two.count == len(flock_two.geese)
    expected_lucky = int(
        sum(goose.lucky for goose in flock_two.geese) / len(flock_two.geese),
    )
    assert flock_two.lucky == expected_lucky


@pytest.mark.parametrize(
    ('use_war', 'use_honk', 'expect_war_count', 'expect_honk_count'),
    [
        (True, False, 2, 0),
        (False, True, 0, 2),
    ],
)
def test_flock_basic_configurations(
    use_war: bool,
    use_honk: bool,
    expect_war_count: int,
    expect_honk_count: int,
    war1: WarGoose,
    war2: WarGoose,
    honk1: HonkGoose,
    honk2: HonkGoose,
) -> None:
    # сборка стаи
    geese: list[Goose] = []
    if use_war:
        geese.extend([war1, war2])
    if use_honk:
        geese.extend([honk1, honk2])

    flock = FlockGoose(name='Goose', geese=geese)

    assert len(flock.war) == expect_war_count
    assert len(flock.honk) == expect_honk_count


def test_empty_flock_aggregates() -> None:
    flock = FlockGoose(name='empty', geese=[])

    assert flock.geese == []
    assert flock.war == []
    assert flock.honk == []
    assert flock.count == 0
    assert flock.lucky == 0
    assert flock.honk_volume == 0
    assert flock.strength == 0


def test_empty_flock_actions_produce_no_effects(
    rich_player: Player,
) -> None:
    flock = FlockGoose(name='empty', geese=[])

    assert flock.act_player(rich_player) == []
    assert flock.act_self() == []


def test_flock_with_only_war_geese(
    war1: WarGoose,
    war2: WarGoose,
    rich_player: Player,
) -> None:
    flock = FlockGoose(name='war-only', geese=[war1, war2])

    assert flock.war == [war1, war2]
    assert flock.honk == []
    assert flock.honk_volume == 0
    assert flock.strength == war1.strength + war2.strength

    effects: list[Effect] = flock.act_player(rich_player)

    stun_effects = get_stun_effects(effects)
    steal_effects = get_steal_effects(effects)

    assert not stun_effects
    assert len(steal_effects) == 1 + len(flock.war)


def test_flock_with_only_honk_geese(
    honk1: HonkGoose,
    honk2: HonkGoose,
    rich_player: Player,
) -> None:
    flock = FlockGoose(name='honk-only', geese=[honk1, honk2])

    assert flock.war == []
    assert flock.honk == [honk1, honk2]
    assert flock.strength == 0
    expected_honk_volume = int(
        (honk1.honk_volume + honk2.honk_volume) / 2,
    )
    assert flock.honk_volume == expected_honk_volume

    effects_player: list[Effect] = flock.act_player(rich_player)
    effects_self: list[Effect] = flock.act_self()

    assert get_stun_effects(effects_player)
    assert not get_steal_effects(effects_player)

    assert get_stun_effects(effects_self)
    assert not get_steal_effects(effects_self)


def test_flock_big_strength_and_balance(
    rich_player: Player,
) -> None:
    big_strength = 10**12
    war = WarGoose(name='big-war', strength=big_strength)
    flock = FlockGoose(name='big-flock', geese=[war])

    rich_player.balance = 10**12 + 123

    effects: list[Effect] = flock.act_player(rich_player)
    steal_effects = get_steal_effects(effects)

    assert len(steal_effects) == 2

    player_steal = next(
        effect for effect in steal_effects if effect.target is rich_player
    )
    war_steal = next(effect for effect in steal_effects if effect.target is war)

    expected_steal = min(flock.strength, rich_player.balance)
    assert expected_steal == big_strength
    assert player_steal.delta == -expected_steal
    assert war_steal.delta == expected_steal


def test_flock_act_player_does_not_mutate_flock(
    flock_four: FlockGoose,
    rich_player: Player,
) -> None:
    before_geese = tuple(flock_four.geese)
    before_war = tuple(flock_four.war)
    before_honk = tuple(flock_four.honk)
    before_lucky = flock_four.lucky
    before_honk_volume = flock_four.honk_volume
    before_strength = flock_four.strength
    before_count = flock_four.count
    before_war_balances = tuple(w.balance for w in flock_four.war)

    _ = flock_four.act_player(rich_player)

    assert tuple(flock_four.geese) == before_geese
    assert tuple(flock_four.war) == before_war
    assert tuple(flock_four.honk) == before_honk
    assert flock_four.lucky == before_lucky
    assert flock_four.honk_volume == before_honk_volume
    assert flock_four.strength == before_strength
    assert flock_four.count == before_count
    assert tuple(w.balance for w in flock_four.war) == before_war_balances


def test_flock_act_player_preserves_total_balance_for_player_and_war(
    flock_four: FlockGoose,
    rich_player: Player,
) -> None:
    before_total = rich_player.balance + sum(w.balance for w in flock_four.war)

    effects: list[Effect] = flock_four.act_player(rich_player)
    steal_effects = get_steal_effects(effects)

    for effect in steal_effects:
        effect.on_tick()

    after_total = rich_player.balance + sum(w.balance for w in flock_four.war)
    assert after_total == before_total
