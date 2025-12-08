from dataclasses import dataclass
from typing import Protocol

from domain.goose import Goose
from domain.player import BalanceInterface, Player


class Effect(Protocol):
    duration: int

    def on_tick(self) -> None:
        """
        Глобальный тик для конкретного эффекта
        Например, уменьшает duration
        """
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


@dataclass
class StunEffect:
    source: Goose
    target: Goose | Player
    duration: int

    def on_tick(self) -> None:
        # Просто тикает таймер
        # Casino проверяет наличие StunEffect, чтобы запретить действия
        self.duration -= 1
