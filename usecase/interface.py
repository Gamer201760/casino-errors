from typing import Iterator, Protocol, overload

from domain.effect import Effect
from domain.engine import EffectEngine
from domain.goose import Goose
from domain.player import Player


class PlayerCollection(Protocol):
    """Интерфейс коллекции игроков"""

    def add(self, player: Player) -> None: ...
    def remove(self, player: Player) -> None: ...

    def __iter__(self) -> Iterator[Player]: ...
    def __len__(self) -> int: ...

    @overload
    def __getitem__(self, index: int) -> Player: ...
    @overload
    def __getitem__(self, index: slice) -> list[Player]: ...
    def __getitem__(self, index: int | slice) -> Player | list[Player]: ...


class GooseCollection(Protocol):
    """Интерфейс коллекции гусей"""

    def add(self, goose: Goose) -> None: ...
    def remove(self, goose: Goose) -> None: ...

    def __iter__(self) -> Iterator[Goose]: ...
    def __len__(self) -> int: ...

    @overload
    def __getitem__(self, index: int) -> Goose: ...
    @overload
    def __getitem__(self, index: slice) -> list[Goose]: ...
    def __getitem__(self, index: int | slice) -> Goose | list[Goose]: ...


class CasinoBalance(Protocol):
    """
    Интерфейс для словарной коллекции балансов (игрок/гусь -> баланс)
    """

    def __getitem__(self, key: str) -> int: ...
    def __setitem__(self, key: str, value: int) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...


class CasinoStatistic(Protocol):
    """Интерфейс для статистики игры"""

    def on_init(
        self,
        *,
        players: PlayerCollection,
        geese: GooseCollection,
        casino_bank: int,
    ) -> None: ...

    def on_step_begin(
        self,
        *,
        step: int,
        players: PlayerCollection,
        geese: GooseCollection,
        effects: EffectEngine,
        casino_bank: int,
    ) -> None: ...

    def on_event_selected(self, *, step: int, event_name: str) -> None: ...

    def on_bet(
        self,
        *,
        step: int,
        player: Player,
        bet: int,
        win: bool,
        multiplier: int,
        payout: int,
        casino_bank: int,
    ) -> None: ...

    def on_attack(
        self,
        *,
        step: int,
        goose: Goose,
        attacked_self: bool,
    ) -> None: ...

    def on_flock_create(self, *, step: int, size: int) -> None: ...

    def on_tick_end(
        self,
        *,
        step: int,
        effects: list[Effect],
        casino_bank: int,
    ) -> None: ...
