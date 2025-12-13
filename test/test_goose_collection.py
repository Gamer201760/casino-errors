import pytest

from domain.goose import Goose
from usecase.interface import GooseCollection


def test_goose_collection_add(
    war1: Goose,
    goose_collection: GooseCollection,
) -> None:
    goose_collection.add(war1)

    assert len(goose_collection) == 1
    assert goose_collection[0] == war1
    assert war1 in goose_collection


def test_goose_collection_remove(
    war1: Goose,
    goose_collection: GooseCollection,
) -> None:
    goose_collection.add(war1)

    goose_collection.remove(war1)

    assert len(goose_collection) == 0
    assert war1 not in goose_collection


def test_goose_collection_remove_missing_raises_error(
    war1: Goose,
    goose_collection: GooseCollection,
) -> None:
    with pytest.raises(ValueError):
        goose_collection.remove(war1)


def test_goose_collection_indexing(
    war1: Goose,
    honk1: Goose,
    goose_collection: GooseCollection,
) -> None:
    goose_collection.add(war1)
    goose_collection.add(honk1)

    assert goose_collection[0] == war1
    assert goose_collection[1] == honk1

    with pytest.raises(IndexError):
        _ = goose_collection[2]


def test_goose_collection_slicing(
    war1: Goose,
    honk1: Goose,
    goose_collection: GooseCollection,
) -> None:
    goose_collection.add(war1)
    goose_collection.add(honk1)

    slice_result = goose_collection[1:]

    assert isinstance(slice_result, list)
    assert len(slice_result) == 1
    assert slice_result[0] == honk1


def test_goose_collection_iteration(
    war1: Goose,
    honk1: Goose,
    goose_collection: GooseCollection,
) -> None:
    goose_collection.add(war1)
    goose_collection.add(honk1)

    items = list(goose_collection)

    assert items == [war1, honk1]
