from dataclasses import dataclass
from typing import Protocol

from domain.effect import Effect, OnceStealBalance, StunEffect
from domain.player import Player


class Goose(Protocol):
    name: str
    lucky: int

    def act_player(self, player: Player) -> list[Effect]: ...
    def act_self(self) -> list[Effect]: ...

    def __add__(self, other: 'Goose') -> 'FlockGoose': ...


class FlockGoose(Goose): ...


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

    def __add__(self, other: 'Goose') -> 'FlockGoose': ...


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

    def __add__(self, other: 'Goose') -> 'FlockGoose': ...
