from adapter.cli.utils import gen_random_geese, gen_random_players
from usecase.casino import Casino


def run_simulation(casino: Casino, *, steps: int = 20) -> None:
    for p in gen_random_players(casino._config):
        casino.register_player(p)

    for g in gen_random_geese(casino._config):
        casino.register_goose(g)

    for _ in range(steps):
        casino.step()
