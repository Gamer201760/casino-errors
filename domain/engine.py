from domain.effect import Effect
from domain.entity import Entity
from domain.goose import Goose
from domain.player import Player


class EffectEngine:
    def __init__(self) -> None:
        self._effects: dict[str, list[Effect]] = {}

    def add_effect(self, effect: Effect) -> None:
        key = self._key_of_target(effect.target)
        bucket = self._effects.get(key)
        if bucket is None:
            self._effects[key] = [effect]
            return
        bucket.append(effect)

    def tick(self) -> None:
        for key, bucket in self._effects.items():
            alive: list[Effect] = []

            for eff in bucket:
                if eff.duration <= 0:
                    continue

                eff.on_tick()

                if eff.duration > 0:
                    alive.append(eff)

            if alive:
                self._effects[key] = alive
            else:
                self._effects.pop(key, None)

    def check_effect(self, target: Entity, effect_type: type[Effect]) -> bool:
        key = self._key_of_target(target)
        bucket = self._effects.get(key, [])

        for eff in bucket:
            if isinstance(eff, effect_type) and eff.duration > 0:
                return True
        return False

    def _key_of_target(self, entity: Entity) -> str:
        if isinstance(entity, Player):
            return f'player:{entity.name}'

        if isinstance(entity, Goose):
            return f'goose:{entity.name}'

        return str(id(entity))
