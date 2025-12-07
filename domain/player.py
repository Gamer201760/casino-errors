from dataclasses import dataclass

from domain.entity import Entity


@dataclass
class Player(Entity):
    name: str
    balance: int = 0
    lucky: int = 0
    stun: int = 0

    def apply_stun(self, turns: int) -> None:
        self.stun = max(self.stun, turns)

    def change_balance(self, delta: int) -> None:
        self.balance += delta

    def is_stunned(self) -> bool:
        return self.stun > 0

    def tick(self) -> None:
        if self.stun > 0:
            self.stun -= 1
