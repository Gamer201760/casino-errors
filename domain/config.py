from dataclasses import dataclass, fields
from pathlib import Path

import yaml


@dataclass(slots=True, frozen=True)
class CasinoConfig:
    seed: int | None = None

    generate_player_count: int = 30
    generate_player_max_bal: int = 100
    generate_player_max_lucky: int = 40

    generate_goose_count: int = 30
    generate_war_goose_p: float = 0.5
    generate_goose_max_lucky: int = 20
    generate_goose_max_bal: int = 100
    generate_goose_max_strenght: int = 30
    generate_goose_max_honk_volume: int = 30

    casino_base_bal: int = 100
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

    def __post_init__(self) -> None:
        normalized_seed = (
            None if (self.seed is not None and self.seed < 1) else self.seed
        )
        object.__setattr__(self, 'seed', normalized_seed)  # Костыль чтобы обойти frozen

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
            raise TypeError(f'YAML должен быть словарём, а не: {type(raw).__name__}')

        # Чтобы не допустить случайных ключей в YAML
        allowed = set(x.name for x in fields(cls))
        unknown = set(raw.keys()) - allowed
        if unknown:
            raise ValueError(f'Неизвестный параметр в конфиге: {sorted(unknown)}')

        return cls(**raw).with_defaults()
