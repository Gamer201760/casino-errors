import pytest

from domain.goose import Goose
from repository.goose_collection import InMemoryGooseCollection


def test_goose_collection_add(war1: Goose) -> None:
    collection = InMemoryGooseCollection()

    collection.add(war1)

    assert len(collection) == 1
    assert collection[0] == war1
    assert war1 in collection


def test_goose_collection_remove(war1: Goose) -> None:
    collection = InMemoryGooseCollection()
    collection.add(war1)

    collection.remove(war1)

    assert len(collection) == 0
    assert war1 not in collection


def test_goose_collection_remove_missing_raises_error(war1: Goose) -> None:
    collection = InMemoryGooseCollection()

    with pytest.raises(ValueError):
        collection.remove(war1)


def test_goose_collection_indexing(war1: Goose, honk1: Goose) -> None:
    collection = InMemoryGooseCollection()
    collection.add(war1)
    collection.add(honk1)

    assert collection[0] == war1
    assert collection[1] == honk1

    with pytest.raises(IndexError):
        _ = collection[2]


def test_goose_collection_slicing(war1: Goose, honk1: Goose) -> None:
    collection = InMemoryGooseCollection()
    collection.add(war1)
    collection.add(honk1)

    slice_result = collection[1:]

    assert isinstance(slice_result, list)
    assert len(slice_result) == 1
    assert slice_result[0] == honk1


def test_goose_collection_iteration(war1: Goose, honk1: Goose) -> None:
    collection = InMemoryGooseCollection()
    collection.add(war1)
    collection.add(honk1)

    items = list(collection)

    assert items == [war1, honk1]
