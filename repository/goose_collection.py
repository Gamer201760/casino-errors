from dataclasses import dataclass, field
from typing import Iterator, overload

from domain.goose import Goose
from usecase.interface import GooseCollection


@dataclass
class InMemoryGooseCollection(GooseCollection):
    """
    In-memory реализация коллекции гусей
    Поддерживает добавление, удаление, итерацию, индексацию и срезы
    """

    _geese: list[Goose] = field(default_factory=list)

    def add(self, goose: Goose) -> None:
        self._geese.append(goose)

    def remove(self, goose: Goose) -> None:
        self._geese.remove(goose)

    def __iter__(self) -> Iterator[Goose]:
        return iter(self._geese)

    def __len__(self) -> int:
        return len(self._geese)

    @overload
    def __getitem__(self, index: int) -> Goose: ...
    @overload
    def __getitem__(self, index: slice) -> list[Goose]: ...

    def __getitem__(self, index: int | slice) -> Goose | list[Goose]:
        return self._geese[index]
