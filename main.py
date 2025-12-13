import logging
import random

from domain.goose import HonkGoose, WarGoose
from domain.player import Player
from repository.casino_balance import InMemoryCasinoBalance
from repository.goose_collection import InMemoryGooseCollection
from repository.player_collection import InMemoryPlayerCollection
from usecase.casino import Casino, run_simulation

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] - %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='main.log',
)

logger = logging.getLogger(__name__)

names = [
    'Вадим',
    'Валентин',
    'Валерий',
    'Василий',
    'Виктор',
    'Виталий',
    'Владимир',
    'Владислав',
    'Всеволод',
    'Вячеслав',
    'Максим',
    'Матвей',
    'Михаил',
    'Павел',
    'Пётр',
    'Анна',
    'Мария',
    'Елена',
    'Ольга',
    'Татьяна',
    'Наталья',
    'Екатерина',
    'Ирина',
    'Светлана',
    'Юлия',
    'Дарья',
    'Анастасия',
    'Ксения',
    'Марина',
    'Алёна',
]


def gen_random_player(name: str, max_bal: int = 100) -> Player:
    return Player(name=name, balance=random.randint(1, 100))


def gen_random_players() -> list[Player]:
    players = []
    return players


def main():
    logger.info('Hello from casino!')

    players = InMemoryPlayerCollection()
    players.add(Player(name='Azamat', balance=100, lucky=1))

    goose = InMemoryGooseCollection()
    goose.add(WarGoose(name='LOX', strength=5))
    goose.add(HonkGoose(name='XYI', honk_volume=30))

    balance = InMemoryCasinoBalance()

    casino = Casino(players, goose, balance, balance=100)
    run_simulation(casino)


if __name__ == '__main__':
    try:
        main()
    finally:
        logger.info('Goodbye!')
