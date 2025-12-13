from dataclasses import dataclass, field
from typing import Iterator, overload

from domain.player import Player
from usecase.interface import PlayerCollection


@dataclass
class InMemoryPlayerCollection(PlayerCollection):
    """
    In-memory реализация коллекции игроков
    Поддерживает добавление, удаление, итерацию, индексацию и срезы
    """

    _players: list[Player] = field(default_factory=list)

    def add(self, player: Player) -> None:
        self._players.append(player)

    def remove(self, player: Player) -> None:
        self._players.remove(player)

    def __iter__(self) -> Iterator[Player]:
        return iter(self._players)

    def __len__(self) -> int:
        return len(self._players)

    @overload
    def __getitem__(self, index: int) -> Player: ...
    @overload
    def __getitem__(self, index: slice) -> list[Player]: ...

    def __getitem__(self, index: int | slice) -> Player | list[Player]:
        return self._players[index]
