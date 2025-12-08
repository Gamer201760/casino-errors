from typing import Protocol


class Effect(Protocol):
    duration: int

    def on_tick(self) -> None:
        """
        Глобальный тик для конкретного эффекта
        Например, уменьшает duration
        """
        raise NotImplementedError
