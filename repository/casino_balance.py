from logging import getLogger
from typing import Iterator

from usecase.interface import CasinoBalanceProtocol

logger = getLogger(__name__)


class InMemoryCasinoBalance(CasinoBalanceProtocol):
    """
    Реализация словарной коллекции балансов
    Хранит баланс по имени
    Логирует изменения при записи
    """

    def __init__(self) -> None:
        self._data: dict[str, int] = {}

    def __getitem__(self, key: str) -> int:
        return self._data[key]

    def __setitem__(self, key: str, value: int) -> None:
        logger.info(f'[BALANCE UPDATE] {key}: {self._data.get(key, 0)} -> {value}')
        self._data[key] = value

    def __delitem__(self, key: str) -> None:
        del self._data[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)
