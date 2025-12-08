from dataclasses import dataclass

from domain.effect import Effect
from domain.goose import FlockGoose, Goose
from domain.player import BalanceInterface, Player


class OnceStealBalance:
    def __init__(self, source: Goose, target: BalanceInterface, delta: int) -> None:
        self._source = source
        self._target = target
        self._delta = delta
        self.duration = 1

    def on_tick(self) -> None:
        if self.duration > 0:
            self._target.change_balance(self._delta)
        self.duration -= 1


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
