from dataclasses import dataclass
from typing import Protocol

from domain.entity import Entity
from domain.player import BalanceInterface


class Effect(Protocol):
    duration: int

    def on_tick(self) -> None:
        """
        Глобальный тик для конкретного эффекта
        Например, уменьшает duration
        """
        raise NotImplementedError


@dataclass
class StunEffect:
    source: Entity
    target: Entity
    duration: int

    def on_tick(self) -> None:
        # Просто тикает таймер
        # Casino проверяет наличие StunEffect, чтобы запретить действия
        self.duration -= 1


class OnceStealBalance:
    def __init__(self, source: Entity, target: BalanceInterface, delta: int) -> None:
        self._source = source
        self._target = target
        self._delta = delta
        self.duration = 1

    def on_tick(self) -> None:
        if self.duration > 0:
            self._target.change_balance(self._delta)
        self.duration -= 1
