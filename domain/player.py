from dataclasses import dataclass
from typing import Protocol


class BalanceInterface(Protocol):
    def change_balance(self, delta: int) -> None:
        raise NotImplementedError


@dataclass
class Player:
    name: str
    balance: int = 0
    lucky: int = 0

    def change_balance(self, delta: int) -> None:
        self.balance += delta
