import logging

from domain.config import CasinoConfig
from repository.casino_balance import InMemoryCasinoBalance
from repository.goose_collection import InMemoryGooseCollection
from repository.player_collection import InMemoryPlayerCollection
from usecase.casino import Casino
from utils.random import gen_random_geese, gen_random_players

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] - %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='main.log',
)

logger = logging.getLogger(__name__)


def run_simulation(casino: Casino, *, steps: int = 20) -> None:
    for p in gen_random_players(casino._config):
        casino.register_player(p)

    for g in gen_random_geese(casino._config):
        casino.register_goose(g)

    for _ in range(steps):
        casino.step()


def main():
    logger.info('Hello from casino!')
    cfg = CasinoConfig.from_file('config.yaml')
    logger.debug(f'Конфиг загружен {cfg}')

    players = InMemoryPlayerCollection()
    goose = InMemoryGooseCollection()
    balance = InMemoryCasinoBalance()

    casino = Casino(players, goose, balance, balance=100, config=cfg)
    run_simulation(casino)


if __name__ == '__main__':
    try:
        main()
    finally:
        logger.info('Goodbye!')
