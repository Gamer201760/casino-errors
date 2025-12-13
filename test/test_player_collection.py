import pytest

from domain.player import Player
from repository.player_collection import InMemoryPlayerCollection


def test_player_collection_add(rich_player: Player) -> None:
    collection = InMemoryPlayerCollection()

    collection.add(rich_player)

    assert len(collection) == 1
    assert collection[0] == rich_player
    assert rich_player in collection


def test_player_collection_remove(rich_player: Player) -> None:
    collection = InMemoryPlayerCollection()
    collection.add(rich_player)

    collection.remove(rich_player)

    assert len(collection) == 0
    assert rich_player not in collection


def test_player_collection_remove_missing_raises_error(rich_player: Player) -> None:
    collection = InMemoryPlayerCollection()

    with pytest.raises(ValueError):
        collection.remove(rich_player)


def test_player_collection_indexing(rich_player: Player, poor_player: Player) -> None:
    collection = InMemoryPlayerCollection()
    collection.add(rich_player)
    collection.add(poor_player)

    assert collection[0] == rich_player
    assert collection[1] == poor_player

    with pytest.raises(IndexError):
        _ = collection[2]


def test_player_collection_slicing(rich_player: Player, poor_player: Player) -> None:
    collection = InMemoryPlayerCollection()
    collection.add(rich_player)
    collection.add(poor_player)

    slice_result = collection[0:1]

    assert isinstance(slice_result, list)
    assert len(slice_result) == 1
    assert slice_result[0] == rich_player


def test_player_collection_iteration(rich_player: Player, poor_player: Player) -> None:
    collection = InMemoryPlayerCollection()
    collection.add(rich_player)
    collection.add(poor_player)

    items = list(collection)

    assert items == [rich_player, poor_player]
