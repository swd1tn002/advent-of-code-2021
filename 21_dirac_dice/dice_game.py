from typing import Tuple
import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


def read_players() -> Tuple['Player']:
    """
    Each player's starting space is chosen randomly (your puzzle input).
    The last character on the first two lines marks the starting positions
    of the players.
    """
    with open(INPUT_FILE) as file:
        puzzle_input = file.read().split('\n')

    p0 = Player(int(puzzle_input[0][-1]))
    p1 = Player(int(puzzle_input[1][-1]))
    return p0, p1


class Player:
    """
    On each player's turn, the player rolls the die three times and adds up the results.
    Then, the player moves their pawn that many times forward around the track.

    After each player moves, they increase their score by the value of the space their
    pawn stopped on. Players' scores start at 0.
    """

    def __init__(self, position, score=0):
        self.position = position
        self.score = score

    def apply_steps(self, amount) -> 'Player':
        """
        Returns a new Player object with the given dice amount added to
        the position and score of this Player.
        """
        new_pos = (self.position + amount - 1) % 10 + 1
        return Player(new_pos, self.score + new_pos)


class Dice:
    """
    This die always rolls 1 first, then 2, then 3, and so
    on up to 100, after which it starts over at 1 again.
    """

    def __init__(self):
        self.counter = 0

    def roll(self):
        self.counter += 1
        return (self.counter-1) % 100 + 1


if __name__ == '__main__':
    p0, p1 = read_players()

    dice = Dice()
    turn = 0

    while p0.score < 1_000 and p1.score < 1_000:
        steps = sum(dice.roll() for i in range(3))

        if turn % 2 == 0:
            p0 = p0.apply_steps(steps)
        else:
            p1 = p1.apply_steps(steps)

        turn += 1

    print('Scores after the game:', p0.score, p1.score)

    # The moment either player wins, what do you get if you multiply the score of
    # the losing player by the number of times the die was rolled during the game?
    # => 1067724
    print(f'Part 1: {min(p0.score, p1.score) * dice.counter}')
