from random import Random

from domain.config import CasinoConfig
from domain.goose import Goose, HonkGoose, WarGoose
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
    if cfg.generate_player_count > len(NAMES):
        raise ValueError(
            f'generate_player_count={cfg.generate_player_count} больше чем доступных имён={len(NAMES)}'
        )
    return [
        gen_random_player(name, cfg)
        for name in Random(cfg.seed).sample(NAMES, cfg.generate_player_count)
    ]


def gen_random_goose(
    name: str,
    cfg: CasinoConfig,
    rng: Random,
) -> Goose:
    lucky = rng.randint(1, cfg.generate_goose_max_lucky)
    balance = rng.randint(0, cfg.generate_goose_max_bal)

    if rng.random() < cfg.generate_war_goose_p:
        strength = rng.randint(1, cfg.generate_goose_max_strenght)
        return WarGoose(
            name=name,
            strength=strength,
            lucky=lucky,
            balance=balance,
        )

    honk_volume = rng.randint(1, cfg.generate_goose_max_honk_volume)
    return HonkGoose(
        name=name,
        honk_volume=honk_volume,
        lucky=lucky,
        balance=balance,
    )


def gen_random_geese(cfg: CasinoConfig) -> list[Goose]:
    if cfg.generate_goose_count > len(NAMES):
        raise ValueError(
            f'generate_goose_count={cfg.generate_goose_count} больше чем доступных имён={len(NAMES)}'
        )

    rng = Random(cfg.seed)
    chosen_names = rng.sample(NAMES, cfg.generate_goose_count)
    return [gen_random_goose(name, cfg, rng) for name in chosen_names]
