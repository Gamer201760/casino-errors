from random import Random

from adapter.cli.utils import gen_random_geese, gen_random_players
from domain.config import CasinoConfig
from usecase.casino import Casino


def run_simulation(
    cfg: CasinoConfig, casino: Casino, rng: Random, *, steps: int = 20
) -> None:
    for p in gen_random_players(cfg, rng):
        casino.register_player(p)

    for g in gen_random_geese(cfg, rng):
        casino.register_goose(g)

    for _ in range(steps):
        casino.step()
