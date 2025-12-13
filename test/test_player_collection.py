import pytest

from domain.player import Player
from usecase.interface import PlayerCollection


def test_player_collection_add(
    rich_player: Player,
    player_collection: PlayerCollection,
) -> None:
    player_collection.add(rich_player)

    assert len(player_collection) == 1
    assert player_collection[0] == rich_player
    assert rich_player in player_collection


def test_player_collection_remove(
    rich_player: Player,
    player_collection: PlayerCollection,
) -> None:
    player_collection.add(rich_player)

    player_collection.remove(rich_player)

    assert len(player_collection) == 0
    assert rich_player not in player_collection


def test_player_collection_remove_missing_raises_error(
    rich_player: Player,
    player_collection: PlayerCollection,
) -> None:
    with pytest.raises(ValueError):
        player_collection.remove(rich_player)


def test_player_collection_indexing(
    rich_player: Player,
    poor_player: Player,
    player_collection: PlayerCollection,
) -> None:
    player_collection.add(rich_player)
    player_collection.add(poor_player)

    assert player_collection[0] == rich_player
    assert player_collection[1] == poor_player

    with pytest.raises(IndexError):
        _ = player_collection[2]


def test_player_collection_slicing(
    rich_player: Player,
    poor_player: Player,
    player_collection: PlayerCollection,
) -> None:
    player_collection.add(rich_player)
    player_collection.add(poor_player)

    slice_result = player_collection[0:1]

    assert isinstance(slice_result, list)
    assert len(slice_result) == 1
    assert slice_result[0] == rich_player


def test_player_collection_iteration(
    rich_player: Player,
    poor_player: Player,
    player_collection: PlayerCollection,
) -> None:
    player_collection.add(rich_player)
    player_collection.add(poor_player)

    items = list(player_collection)

    assert items == [rich_player, poor_player]
