import argparse
import logging
from random import Random

from adapter.cli.report import print_statistic_report
from adapter.cli.simulation import run_simulation
from domain.config import CasinoConfig
from repository.casino_balance import InMemoryCasinoBalance
from repository.goose_collection import InMemoryGooseCollection
from repository.stats import Statistic
from usecase.casino import Casino
from usecase.interface import PlayerCollection

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] - %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='casino.log',
)

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Симуляция казино с гусями',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '--steps',
        type=int,
        default=200,
        help='количество шагов симуляции',
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    logger.info('Hello from casino!')
    cfg = CasinoConfig.from_file('config.yaml')
    logger.debug(f'Конфиг загружен {cfg}')

    players = PlayerCollection()
    goose = InMemoryGooseCollection()
    balance = InMemoryCasinoBalance()
    stats = Statistic()
    rng = Random(cfg.seed)

    casino = Casino(players, goose, balance, rng=rng, stat=stats, config=cfg)
    run_simulation(cfg, casino, rng, steps=args.steps)
    print_statistic_report(
        stats,
        players=players,
        geese=goose,
        casino_bank=casino.balance,
    )


if __name__ == '__main__':
    try:
        main()
    finally:
        logger.info('Goodbye!')
