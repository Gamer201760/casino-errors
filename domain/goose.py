from typing import Protocol

from domain.effect import Effect
from domain.player import Player


class Goose(Protocol):
    name: str
    lucky: int

    def act_player(self, player: Player) -> list[Effect]: ...
    def act_self(self) -> list[Effect]: ...

    def __add__(self, other: 'Goose') -> 'FlockGoose': ...


class FlockGoose(Goose): ...
