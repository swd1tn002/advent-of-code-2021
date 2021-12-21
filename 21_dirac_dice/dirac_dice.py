from collections import Counter
from typing import Tuple
from dice_game import read_players, Player
import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


def count_combinations() -> Counter:
    """
    Returns a Counter that counts the possible sums for a three-sided dice and
    the count of different combinations for each.

    For example {4: 3} because 4 can be thrown as 1+1+2, 1+2+1 or 2+1+1
    """
    counter = Counter()
    for d1 in (1, 2, 3):
        for d2 in (1, 2, 3):
            for d3 in (1, 2, 3):
                counter[d1+d2+d3] += 1
    return counter


# Values that can be thrown with three 3-sided dices and their different combinations (universes).
dice_universes = count_combinations()
dice_sums = dice_universes.keys()


def play_dirac_dice(p0: Player, p1: Player):
    """
    An informational brochure in the compartment explains that this is a quantum die:
    when you roll it, the universe splits into multiple copies, one copy for each
    possible outcome of the die. Using your given starting positions, determine every 
    possible outcome.

    Returns a Counter with keys 0 and 1 containing the number of winning universes for
    players 0 and 1.
    """

    wins = Counter()

    for p0_dice in dice_sums:
        # this is a quantum die: when you roll it, the universe splits into multiple copies
        universes = dice_universes.get(p0_dice)

        p0_next = p0.apply_steps(p0_dice)

        if p0_next.score >= 21:
            # Player 0 wins in this many parallel universes
            wins[0] += universes
        else:
            for p1_dice in dice_sums:
                # each copy of the previous universes splits again into new copies
                universes = dice_universes.get(
                    p0_dice) * dice_universes.get(p1_dice)

                p1_next = p1.apply_steps(p1_dice)

                if p1_next.score >= 21:
                    # Player 1 wins in this many parallel universes
                    wins[1] += universes
                else:
                    # play new turn
                    new_wins = play_dirac_dice(p0_next, p1_next)

                    wins[0] += universes * new_wins[0]
                    wins[1] += universes * new_wins[1]

    return wins


if __name__ == '__main__':
    p0, p1 = read_players()
    wins = play_dirac_dice(p0, p1)

    print(f'Wins: {wins[0]} {wins[1]}')

    # Find the player that wins in more universes; in how many universes does that player win?
    # => 630947104784464
    print(f'Part 2: the most winning universes is {max(wins.values())}')
