from domain.player import Player


def test_player_change_balance_positive():
    player = Player(name='p', balance=10)
    player.change_balance(5)
    assert player.balance == 15


def test_player_change_balance_negative():
    player = Player(name='p', balance=10)
    player.change_balance(-7)
    assert player.balance == 3
