from dice_game import read_players, Dice
from dirac_dice import count_combinations


def test_read_players():
    p0, p1 = read_players()

    assert p0.score == 0
    assert p1.score == 0

    assert p0.position == 5
    assert p1.position == 8


def test_rolling_dice():
    """
    This die always rolls 1 first, then 2, then 3, and so on up to 100, after which it starts over at 1 again.
    """
    dice = Dice()

    assert dice.roll() == 1
    assert dice.roll() == 2
    assert dice.roll() == 3


def test_count_combinations():
    combinations = count_combinations()

    assert combinations.keys() == {3, 4, 5, 6, 7, 8, 9}

    assert combinations[3] == 1
    assert combinations[4] == 3
    assert combinations[9] == 1
