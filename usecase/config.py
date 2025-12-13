from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CasinoConfig:
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
