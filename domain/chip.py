from dataclasses import dataclass


@dataclass
class Chip:
    value: int

    def __add__(self, other: 'Chip') -> 'Chip':
        return Chip(self.value + other.value)
