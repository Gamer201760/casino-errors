import pytest

from domain.honk_goose import HonkGoose
from domain.player import Player
from domain.war_goose import WarGoose


@pytest.fixture
def player_zero() -> Player:
    return Player(name='player', balance=0, lucky=0)


@pytest.fixture
def player_rich() -> Player:
    return Player(name='rich', balance=100, lucky=0)


@pytest.fixture
def war_goose_strong() -> WarGoose:
    return WarGoose(name='war', strength=50, lucky=0, balance=0)


@pytest.fixture
def war_goose_weak() -> WarGoose:
    return WarGoose(name='war_weak', strength=10, lucky=0, balance=0)


@pytest.fixture
def honk_goose_loud() -> HonkGoose:
    return HonkGoose(name='honk', honk_volume=35, lucky=0, balance=0)


@pytest.fixture
def honk_goose_quiet() -> HonkGoose:
    return HonkGoose(name='quiet', honk_volume=5, lucky=0, balance=0)
