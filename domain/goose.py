from dataclasses import dataclass
from typing import Protocol

from domain.effect import Effect, OnceStealBalance, StunEffect
from domain.entity import Entity
from domain.player import Player


class Goose(Entity, Protocol):
    name: str
    lucky: int

    def act_player(self, player: Player) -> list[Effect]: ...
    def act_self(self) -> list[Effect]: ...

    def __add__(self, other: 'Goose') -> 'Goose': ...


@dataclass
class WarGoose(Goose):
    name: str
    strength: int
    lucky: int = 0
    balance: int = 0

    def change_balance(self, delta: int) -> None:
        self.balance += delta

    def act_player(self, player: Player) -> list[Effect]:
        """
        Атакует игрока с некоторым шансем,
        на него влияет удача гуся - удача игрока
        Может атаковать сам себя, тогда его баланс переходит игроку
        """
        steal = min(self.strength, player.balance)

        return [
            # Игрок теряет деньги
            OnceStealBalance(source=self, target=player, delta=-steal),
            # Гусь получает доход
            OnceStealBalance(source=self, target=self, delta=steal),
        ]

    def act_self(self) -> list[Effect]:
        lost = min(self.strength, self.balance)
        if lost <= 0:
            return []
        return [
            OnceStealBalance(source=self, target=self, delta=-lost),
        ]

    def __add__(self, other: Goose) -> Goose:
        if isinstance(other, FlockGoose):
            return other + self
        return FlockGoose(self.name, [self, other])


@dataclass
class HonkGoose(Goose):
    name: str
    honk_volume: int
    lucky: int = 0
    balance: int = 0

    def _stun_turns(self) -> int:
        return max(1, self.honk_volume // 10)

    def act_player(self, player: Player) -> list[Effect]:
        """
        Есть шанс оглушение игрока на (громкость / 10) шагов,
        на него влияет удача гуся - удача игрока,
        иначе оглушает самого себя
        """
        return [
            StunEffect(source=self, target=player, duration=self._stun_turns()),
        ]

    def act_self(self) -> list[Effect]:
        return [
            StunEffect(source=self, target=self, duration=self._stun_turns()),
        ]

    def __add__(self, other: Goose) -> Goose:
        if isinstance(other, FlockGoose):
            return other + self
        return FlockGoose(self.name, [self, other])


class FlockGoose(Goose):
    def __init__(self, name: str, geese: list[Goose]) -> None:
        self._geese = geese
        self.lucky = 0
        self.name = name
        self._strength = 0
        self._honk_volume = 0

    @property
    def _honk_geese(self) -> list[HonkGoose]:
        return [g for g in self._geese if isinstance(g, HonkGoose)]

    @property
    def _war_geese(self) -> list[WarGoose]:
        return [g for g in self._geese if isinstance(g, WarGoose)]

    def act_player(self, player: Player) -> list[Effect]:
        effects: list[Effect] = []

        # 1. Оглушение игрока на среднюю громкость
        if self._honk_volume > 0:
            stun_turns = max(1, self._honk_volume // 10)
            effects.append(
                StunEffect(source=self, target=player, duration=stun_turns),
            )

        # 2. Игрок теряет деньги = суммарная сила всех атакующих гусей
        steal = min(self._strength, player.balance)

        if steal > 0:
            effects.append(
                OnceStealBalance(source=self, target=player, delta=-steal),
            )

            # Деньги распределяются между WarGoose внутри стаи равномерно
            share, rem = (
                divmod(steal, len(self._war_geese)) if self._war_geese else (0, 0)
            )
            for i, w in enumerate(self._war_geese):
                delta = share + (1 if i < rem else 0)
                effects.append(
                    OnceStealBalance(source=self, target=w, delta=delta),
                )

        return effects

    def act_self(self) -> list[Effect]:
        effects: list[Effect] = []

        # 1. Оглушаем каждого гуся стаи
        if self._honk_volume > 0:
            stun_turns = max(1, self._honk_volume // 10)
            for g in self._geese:
                effects.append(
                    StunEffect(source=self, target=g, duration=stun_turns),
                )

        # 2. У каждого атакующего гуся забираем деньги равные суммарной силе
        if self._strength > 0:
            for w in self._war_geese:
                lost = min(w.balance, self._strength)
                if lost > 0:
                    effects.append(
                        OnceStealBalance(source=self, target=w, delta=-lost),
                    )

        return effects

    def __add__(self, other: 'Goose') -> 'Goose':
        self._geese.append(other)
        self.lucky += int(other.lucky / len(self._geese))
        if isinstance(other, WarGoose):
            self._strength += other.strength
        elif isinstance(other, HonkGoose):
            self._honk_volume += int(other.honk_volume / len(self._geese))
        return self
