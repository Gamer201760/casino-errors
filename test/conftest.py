import pytest

from domain.goose import FlockGoose, HonkGoose, WarGoose
from domain.player import Player
from repository.casino_balance import InMemoryCasinoBalance
from usecase.interface import CasinoBalanceProtocol


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


@pytest.fixture
def war1() -> WarGoose:
    return WarGoose(name='war1', strength=10, lucky=2, balance=0)


@pytest.fixture
def war2() -> WarGoose:
    return WarGoose(name='war2', strength=20, lucky=4, balance=0)


@pytest.fixture
def honk1() -> HonkGoose:
    return HonkGoose(name='honk1', honk_volume=10, lucky=6, balance=0)


@pytest.fixture
def honk2() -> HonkGoose:
    return HonkGoose(name='honk2', honk_volume=30, lucky=8, balance=0)


@pytest.fixture
def flock_two(war1, honk1) -> FlockGoose:
    return FlockGoose('flock_two', [war1, honk1])


@pytest.fixture
def flock_four(war1, war2, honk1, honk2) -> FlockGoose:
    return FlockGoose('flock_four', [war1, war2, honk1, honk2])


@pytest.fixture
def rich_player() -> Player:
    return Player(name='rich', balance=100, lucky=0)


@pytest.fixture
def poor_player() -> Player:
    return Player(name='poor', balance=5, lucky=0)


@pytest.fixture
def balance_store() -> CasinoBalanceProtocol:
    return InMemoryCasinoBalance()
