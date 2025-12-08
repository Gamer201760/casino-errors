from typing import Protocol

from domain.goose import Goose


class Effect(Protocol):
    duration: int

    def on_tick(self) -> None:
        """
        Глобальный тик для конкретного эффекта
        Например, уменьшает duration
        """
        raise NotImplementedError


class BalanceInterface(Protocol):
    def change_balance(self, delta: int) -> None:
        raise NotImplementedError


class OnceStealBalance:
    def __init__(self, source: Goose, target: BalanceInterface, delta: int) -> None:
        self._source = source
        self._target = target
        self._delta = delta

    def on_tick(self) -> None:
        if self.duration > 0:
            self._target.change_balance(self._delta)
        self.duration -= 1
