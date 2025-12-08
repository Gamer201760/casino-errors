from domain.effect import OnceStealBalance, StunEffect


def test_flock_aggregates_two_geese(war1, honk1, flock_two):
    flock = flock_two

    assert flock.geese == [war1, honk1]
    assert flock.war == [war1]
    assert flock.honk == [honk1]

    # lucky = среднее по lucky
    expected_lucky = int((war1.lucky + honk1.lucky) / 2)
    assert flock.lucky == expected_lucky

    # _honk_volume = средняя громкость только по HonkGoose
    expected_honk_volume = int(honk1.honk_volume / 1)
    assert flock._honk_volume == expected_honk_volume


def test_flock_aggregates_four_geese(flock_four, war1, war2, honk1, honk2):
    flock = flock_four

    assert len(flock.geese) == 4
    assert war1 in flock.geese
    assert war2 in flock.geese
    assert honk1 in flock.geese
    assert honk2 in flock.geese

    assert len(flock.war) == 2
    assert war1 in flock.war
    assert war2 in flock.war

    assert len(flock.honk) == 2
    assert honk1 in flock.honk
    assert honk2 in flock.honk

    expected_lucky = int((war1.lucky + war2.lucky + honk1.lucky + honk2.lucky) / 4)
    assert flock.lucky == expected_lucky

    expected_honk_volume = int((honk1.honk_volume + honk2.honk_volume) / 2)
    assert flock._honk_volume == expected_honk_volume


def test_flock_act_player_no_balance(flock_four, poor_player):
    flock = flock_four
    player = poor_player
    player.balance = 0

    effects = flock.act_player(player)
    # стан остаётся, кражи нет
    assert any(isinstance(e, StunEffect) for e in effects)
    assert not any(
        isinstance(e, OnceStealBalance) and e.target is player for e in effects
    )


def test_flock_act_self_stuns_all_geese(flock_four):
    flock = flock_four

    effects = flock.act_self()

    stun_effects = [e for e in effects if isinstance(e, StunEffect)]
    assert len(stun_effects) == len(flock.geese)

    expected_turns = max(1, flock._honk_volume // 10)
    for e in stun_effects:
        assert e.source is flock
        assert e.target in flock.geese
        assert e.duration == expected_turns


def test_flock_act_player_with_honk_and_war(flock_four, rich_player):
    flock = flock_four
    player = rich_player

    effects = flock.act_player(player)

    stun_effects = [e for e in effects if isinstance(e, StunEffect)]
    assert len(stun_effects) == 1
    stun = stun_effects[0]
    assert stun.source is flock
    assert stun.target is player

    expected_stun_turns = max(1, flock._honk_volume // 10)
    assert stun.duration == expected_stun_turns

    steal_effects = [e for e in effects if isinstance(e, OnceStealBalance)]
    assert len(steal_effects) == 1 + len(flock.war)

    player_steal = steal_effects[0]
    # поле называется _target
    assert player_steal._target is player

    total_strength = flock._strength
    expected_steal = min(total_strength, rich_player.balance)
    assert player_steal._delta == -expected_steal

    war_deltas = [e._delta for e in steal_effects[1:]]
    assert sum(war_deltas) == expected_steal
    assert len(war_deltas) == len(flock.war)


def test_flock_act_self_steals_from_each_war(flock_four, war1, war2):
    war1.balance = 5
    war2.balance = 100
    flock = flock_four

    effects = flock.act_self()

    steal_effects = [e for e in effects if isinstance(e, OnceStealBalance)]
    assert len(steal_effects) == len(flock.war)

    for e in steal_effects:
        assert e._source is flock
        assert e._target in flock.war
        expected_lost = min(e._target.balance, flock._strength)
        assert e._delta == -expected_lost


def test_flock_add_single_war_updates_aggregates(flock_two, war2):
    flock = flock_two
    result = flock + war2

    assert result is flock
    assert war2 in flock.geese
    assert war2 in flock.war

    expected_lucky = int(sum(g.lucky for g in flock.geese) / len(flock.geese))
    assert flock.lucky == expected_lucky


def test_flock_add_single_honk_updates_honk_volume(flock_two, honk2):
    flock = flock_two
    result = flock + honk2

    assert result is flock
    assert honk2 in flock.geese
    assert honk2 in flock.honk

    expected_honk_volume = int(sum(h.honk_volume for h in flock.honk) / len(flock.honk))
    assert flock._honk_volume == expected_honk_volume


def test_flock_merge_two_flocks(flock_two, flock_four):
    base = flock_two
    other = flock_four

    result = base + other

    assert result is base
    for g in other.geese:
        assert g in base.geese

    assert base._count == len(base.geese)
    expected_lucky = int(sum(g.lucky for g in base.geese) / len(base.geese))
    assert base.lucky == expected_lucky
