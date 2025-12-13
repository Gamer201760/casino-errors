from random import Random

from domain.config import CasinoConfig
from domain.player import Player

NAMES = [
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


def gen_random_player(
    name: str,
    cfg: CasinoConfig,
) -> Player:
    return Player(
        name=name,
        balance=Random(cfg.seed).randint(1, cfg.generate_player_max_bal),
        lucky=Random(cfg.seed).randint(1, cfg.generate_goose_max_lucky),
    )


def gen_random_players(cfg: CasinoConfig) -> list[Player]:
    return [
        gen_random_player(name, cfg)
        for name in Random(cfg.seed).sample(NAMES, cfg.generate_player_count)
    ]
