from typing import Protocol


class Entity(Protocol):
    name: str

    def tick(self) -> None:
        raise NotImplementedError
