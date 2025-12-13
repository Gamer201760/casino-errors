from dataclasses import dataclass

from domain.engine import EffectEngine
from domain.goose import Goose, WarGoose
from domain.player import Player


@dataclass
class MockEffect:
    duration: int
    ticked: int = 0

    def on_tick(self) -> None:
        self.ticked += 1
        self.duration -= 1


@dataclass
class AnotherEffect:
    """Нужен для проверки фильтрации по типу"""

    duration: int = 1

    def on_tick(self) -> None:
        self.duration -= 1


def test_add_and_check_effect_found(engine: EffectEngine, player_zero: Player) -> None:
    effect = MockEffect(duration=2)

    engine.add_effect(player_zero, effect)

    assert engine.check_effect(player_zero, MockEffect) is True


def test_check_effect_not_found_by_type(
    engine: EffectEngine, player_zero: Player
) -> None:
    effect = MockEffect(duration=2)
    engine.add_effect(player_zero, effect)

    # Эффект есть, но другого типа
    assert engine.check_effect(player_zero, AnotherEffect) is False


def test_check_effect_not_found_for_other_entity(
    engine: EffectEngine, player_zero: Player, war1: Goose
) -> None:
    effect = MockEffect(duration=5)
    engine.add_effect(player_zero, effect)

    # У гуся эффекта быть не должно
    assert engine.check_effect(war1, MockEffect) is False


def test_tick_calls_on_tick(engine: EffectEngine, player_zero: Player) -> None:
    effect = MockEffect(duration=5)
    engine.add_effect(player_zero, effect)

    engine.tick()

    assert effect.ticked == 1
    assert effect.duration == 4


def test_tick_removes_expired_effects(
    engine: EffectEngine, player_zero: Player
) -> None:
    # Эффект с длительностью 1 после тика станет 0 и должен удалиться
    effect = MockEffect(duration=1)
    engine.add_effect(player_zero, effect)

    engine.tick()

    # Эффект сработал (duration стал 0)
    assert effect.ticked == 1
    # Движок больше не видит этот эффект
    assert engine.check_effect(player_zero, MockEffect) is False
    # Внутреннее хранилище для этого игрока должно очиститься
    assert engine._effects == {}


def test_tick_keeps_active_effects(engine: EffectEngine, player_zero: Player) -> None:
    effect = MockEffect(duration=2)
    engine.add_effect(player_zero, effect)

    engine.tick()

    # duration стал 1, эффект все еще активен
    assert engine.check_effect(player_zero, MockEffect) is True


def test_multiple_effects_management(engine: EffectEngine, player_zero: Player) -> None:
    short_effect = MockEffect(duration=1)
    long_effect = MockEffect(duration=5)

    engine.add_effect(player_zero, short_effect)
    engine.add_effect(player_zero, long_effect)

    engine.tick()

    # Короткий исчез, длинный остался
    # Проверка через check_effect сложная, так как типы одинаковые
    # Проверим, что длинный сработал
    assert long_effect.ticked == 1
    assert short_effect.ticked == 1

    # Проверим внутреннее состояние: остался только один
    key = engine._key_of_target(player_zero)
    assert len(engine._effects[key]) == 1
    assert engine._effects[key][0] is long_effect


def test_check_effect_ignores_zero_duration(
    engine: EffectEngine, player_zero: Player
) -> None:
    # эффект добавлен, но у него уже 0 (или стало 0 до тика)
    effect = MockEffect(duration=0)
    engine.add_effect(player_zero, effect)

    # check_effect должен проверять duration > 0
    assert engine.check_effect(player_zero, MockEffect) is False


def test_key_generation_logic(engine: EffectEngine) -> None:
    p1 = Player(name='A')
    p2 = Player(name='B')
    g1 = WarGoose(name='A', lucky=1, strength=0)  # Имя совпадает с игроком

    k1 = engine._key_of_target(p1)
    k2 = engine._key_of_target(p2)
    k3 = engine._key_of_target(g1)

    assert k1 == 'player:A'
    assert k2 == 'player:B'
    assert k3 == 'goose:A'

    assert k1 != k2
    assert k1 != k3

    # Неизвестная сущность
    class UnknownEntity:
        pass

    u = UnknownEntity()
    ku = engine._key_of_target(u)
    assert ku == str(id(u))
