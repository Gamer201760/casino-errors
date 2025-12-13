import pytest

from usecase.interface import CasinoBalanceProtocol


def test_balance_set_and_get_item(balance_store: CasinoBalanceProtocol) -> None:
    balance_store['player_1'] = 100

    assert balance_store['player_1'] == 100


def test_balance_overwrite_value(balance_store: CasinoBalanceProtocol) -> None:
    balance_store['player_1'] = 100
    balance_store['player_1'] = 500

    assert balance_store['player_1'] == 500


def test_balance_get_missing_key_raises_error(
    balance_store: CasinoBalanceProtocol,
) -> None:
    with pytest.raises(KeyError):
        _ = balance_store['missing_player']


def test_balance_len(balance_store: CasinoBalanceProtocol) -> None:
    assert len(balance_store) == 0

    balance_store['p1'] = 10
    balance_store['p2'] = 20

    assert len(balance_store) == 2


def test_balance_del_item(balance_store: CasinoBalanceProtocol) -> None:
    balance_store['p1'] = 100

    del balance_store['p1']

    assert len(balance_store) == 0
    with pytest.raises(KeyError):
        _ = balance_store['p1']


def test_balance_del_missing_key_raises_error(
    balance_store: CasinoBalanceProtocol,
) -> None:
    with pytest.raises(KeyError):
        del balance_store['missing_key']


def test_balance_iter(balance_store: CasinoBalanceProtocol) -> None:
    balance_store['p1'] = 10
    balance_store['p2'] = 20
    balance_store['p3'] = 30

    keys = list(balance_store)

    assert len(keys) == 3
    assert 'p1' in keys
    assert 'p2' in keys
    assert 'p3' in keys
