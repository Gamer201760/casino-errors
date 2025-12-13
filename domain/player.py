from dataclasses import dataclass
from typing import Protocol

from domain.entity import Entity


class BalanceInterface(Entity, Protocol):
    balance: int

    def change_balance(self, delta: int) -> None:
        raise NotImplementedError


@dataclass
class Player(Entity):
    name: str
    balance: int = 0
    lucky: int = 0

    def change_balance(self, delta: int) -> None:
        self.balance += delta
