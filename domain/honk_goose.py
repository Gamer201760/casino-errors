from dataclasses import dataclass

from domain.effect import Effect
from domain.goose import FlockGoose, Goose
from domain.player import Player


@dataclass
class StunEffect:
    source: Goose
    target: Goose | Player
    duration: int

    def on_tick(self) -> None:
        # Просто тикает таймер
        # Casino проверяет наличие StunEffect, чтобы запретить действия
        self.duration -= 1


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
