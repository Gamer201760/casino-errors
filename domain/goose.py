from dataclasses import dataclass
from typing import Protocol

from domain.player import Player


class Goose(Protocol):
    name: str
    lucky: int
    balance: int

    def act_player(self, player: Player) -> None: ...
    def act_goose(self, goose: 'Goose') -> None: ...

    def __add__(self, other: 'Goose') -> 'FlockGoose': ...


@dataclass
class FlockGoose(Goose):
    name: str
    geese: list[Goose]
    lucky: int = 0
    balance: int = 0

    def act_player(self, player: Player) -> None:
        for goose in self.geese:
            goose.act_player(player)

    def act_self(self) -> None:
        for goose in self.geese:
            goose.act_self()

    def __add__(self, other: Goose) -> 'FlockGoose':
        self.geese.append(other)
        self.lucky += int(other.lucky / len(self.geese))
        self.balance += other.balance
        return self


@dataclass
class WarGoose(Goose):
    name: str
    strength: int
    lucky: int = 0
    balance: int = 0

    def act_on_player(self, player: Player) -> None:
        """
        Атакует игрока с некоторым шансем,
        на него влияет удача гуся - удача игрока
        Может атаковать сам себя, тогда его баланс переходит игроку
        """
        player.change_balance(-self.strength)


@dataclass
class HonkGoose:
    name: str
    honk_volume: int
    lucky: int = 0
    balance: int = 0

    def act_on_player(self, player: Player) -> None:
        """
        Есть шанс оглушение игрока на (громкость / 10) шагов,
        на него влияет удача гуся - удача игрока,
        иначе оглушает самого себя
        """
        ...
