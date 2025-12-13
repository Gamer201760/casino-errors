from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(slots=True, frozen=True)
class CasinoConfig:
    seed: int = 1

    generate_player_count: int = 30
    generate_player_max_bal: int = 100
    generate_player_lucky_bal: int = 40

    generate_goose_count: int = 30
    generate_war_goose_p: float = 0.5
    generate_goose_lucky_bal: int = 20
    generate_goose_max_bal: int = 100
    generate_goose_max_strenght: int = 30
    generate_goose_max_honk_volume: int = 30

    bet_min: int = 1
    bet_max_fraction: float = 0.30
    bet_win_multiplier_max: int = 4

    bet_win_base: float = 0.50
    bet_win_lucky_scale: float = 0.01

    panic_base: float = 0.50
    panic_lucky_scale: float = 0.005

    self_attack_base: float = 0.15
    self_attack_lucky_scale: float = 0.01

    flock_min_size: int = 2
    flock_max_size: int = 4

    event_weights: dict[str, int] = None  # type: ignore[assignment]

    def with_defaults(self) -> 'CasinoConfig':
        if self.event_weights is not None:
            return self
        return CasinoConfig(
            event_weights={
                'bet': 60,
                'goose_attack': 40,
                'flock_create': 10,
                'flock_disband': 5,
                'panic': 5,
            },
        )

    @classmethod
    def from_file(cls, path: str | Path) -> 'CasinoConfig':
        p = Path(path)
        with p.open('r', encoding='utf-8') as f:
            raw = yaml.safe_load(f)

        if raw is None:
            raw = {}
        if not isinstance(raw, dict):
            raise TypeError(f'YAML root must be a dict, got: {type(raw).__name__}')

        # Создаём дефолтный инстанс, затем применяем значения из файла поверх него
        base = cls().with_defaults()

        data: dict[str, Any] = {**base.__dict__, **raw}

        # Чтобы не допустить случайных ключей в YAML
        allowed = set(cls.__dataclass_fields__.keys())
        unknown = set(data.keys()) - allowed
        if unknown:
            raise ValueError(f'Unknown config keys: {sorted(unknown)}')

        return cls(**data).with_defaults()
