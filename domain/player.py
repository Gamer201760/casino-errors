from dataclasses import dataclass


@dataclass
class Player:
    name: str
    balance: int = 0
    lucky: int = 0

    def change_balance(self, delta: int) -> None:
        self.balance += delta
