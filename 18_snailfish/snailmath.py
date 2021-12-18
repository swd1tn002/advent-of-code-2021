import json
from collections import namedtuple
from typing import List, Tuple
import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

# When exploding, the remains of the Pair are passed around as overflow values
Overflow = namedtuple('Overflow', 'left right')


class Pair:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def plus(self, other: 'Pair') -> 'Pair':
        # make copies to prevent mutations
        return Pair(self.clone(), other.clone())._reduce()

    def clone(self) -> 'Pair':
        return Pair(self.left.clone(), self.right.clone())

    def _reduce(self) -> bool:
        while self.explode(1)[0] or self.split():
            continue
        return self

    def __repr__(self) -> str:
        return f'[{self.left},{self.right}]'

    def __eq__(self, __o: object) -> bool:
        return type(self) == type(__o) and self.left == __o.left and self.right == __o.right

    def explode(self, depth) -> Tuple:
        """
        If any pair is nested inside four pairs, the leftmost such pair explodes.
        """
        if depth == 4:
            return self._do_explode()
        else:
            exploded_left, overflow = self._find_explosions_left(depth)
            if exploded_left:
                return exploded_left, overflow

            exploded_right, overflow = self._find_explosions_right(depth)
            if exploded_right:
                return exploded_right, overflow

            # Neither branch was exploded
            return False, Overflow(None, None)

    def _do_explode(self) -> Tuple:
        """
        To explode a pair, the pair's left value is added to the first regular number to the
        left of the exploding pair (if any), and the pair's right value is added to the first
        regular number to the right of the exploding pair (if any). Exploding pairs will always
        consist of two regular numbers. Then, the entire exploding pair is replaced with the
        regular number 0.
        """
        if type(self.left) == Pair:
            # the pair's right value is added to the first regular number to the right of the exploding pair(if any)
            self.right.increment_leftmost(self.left.right.value)

            overflow = self.left.left
            self.left = Value(0)

            # exploded with overflowing left value
            return True, Overflow(overflow, None)

        elif type(self.right) == Pair:
            # the pair's left value is added to the first regular number to the left of the exploding pair
            self.left.increment_rightmost(self.right.left.value)
            overflow = self.right.right
            self.right = Value(0)

            # exploded with overflowing right value
            return True, Overflow(None, overflow)

        return False, Overflow(None, None)  # not exploded

    def _find_explosions_left(self, depth) -> Tuple:
        exploded_left, overflow = self.left.explode(depth + 1)

        if exploded_left:
            if overflow.left:
                # Can not apply overflow towards left on left node
                return True, overflow

            if overflow.right:
                self.right.increment_leftmost(overflow.right.value)

            # Explosion handled, no overflowing numbers left
            return True, Overflow(None, None)
        else:
            return False, Overflow(None, None)

    def _find_explosions_right(self, depth) -> Tuple:
        exploded_right, overflow = self.right.explode(depth + 1)
        if exploded_right:
            if overflow.right:
                # Can not apply overflow towards right on right node
                return True, overflow

            if overflow.left:
                self.left.increment_rightmost(overflow.left.value)

            # Explosion handled, no overflowing numbers left
            return True, Overflow(None, None)
        else:
            return False, Overflow(None, None)

    def should_split(self) -> bool:
        return self.left.should_split() or self.right.should_split()

    def split(self) -> 'Pair':
        if self.left.should_split():
            self.left = self.left.split()
            return self
        elif self.right.should_split():
            self.right = self.right.split()
            return self
        return None

    def increment_rightmost(self, value):
        self.right.increment_rightmost(value)

    def increment_leftmost(self, value):
        self.left.increment_leftmost(value)

    def magnitude(self) -> int:
        """
        The magnitude of a pair is 3 times the magnitude of its left element
        plus 2 times the magnitude of its right element.
        """
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()


class Value(Pair):
    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        return f'{self.value}'

    def __eq__(self, __o: object) -> bool:
        return type(self) == type(__o) and self.value == __o.value

    def clone(self) -> 'Pair':
        return Value(self.value)

    def explode(self, depth):
        return False, Overflow(None, None)

    def increment_rightmost(self, value):
        self.value += value

    def increment_leftmost(self, value):
        self.value += value

    def should_split(self) -> bool:
        return self.value >= 10

    def split(self) -> Pair:
        """
        To split a regular number, replace it with a pair; the left element of the pair
        should be the regular number divided by two and rounded down, while the right
        element of the pair should be the regular number divided by two and rounded up.
        """
        return Pair(Value(self.value // 2), Value((self.value + 1) // 2))

    def magnitude(self) -> int:
        """
        The magnitude of a regular number is just that number.
        """
        return self.value


def read_puzzle_input(filename=INPUT_FILE) -> List[str]:
    """
    The homework assignment involves adding up a list of snailfish numbers (your puzzle input).
    The snailfish numbers are each listed on a separate line. Add the first snailfish number
    and the second, then add that result and the third, then add that result and the fourth,
    and so on until all numbers in the list have been used once.
    """
    with open(filename) as file:
        return file.read().split('\n')


def parse(formula: str) -> Pair:
    """
    [1,2] => Pair(Value(1), Value(2))
    [[3,4],5] => Pair(Pair(Value(3), Value(4)), Value(5))
    """
    def convert(elem):
        if type(elem) == list:
            return Pair(convert(elem[0]), convert(elem[1]))
        else:
            return Value(elem)

    data = json.loads(formula)
    return convert(data)


if __name__ == '__main__':
    puzzle_input = read_puzzle_input()
    snail_numbers = [parse(line) for line in puzzle_input]

    # Part 1: Add up all of the snailfish numbers from the homework assignment
    # in the order they appear. What is the magnitude of the final sum?
    snail = snail_numbers[0]
    for next_num in snail_numbers[1:]:
        snail = snail.plus(next_num)

    print(f'Part 1: magnitude is {snail.magnitude()}')

    # Part 2: What is the largest magnitude of any sum of two different
    # snailfish numbers from the homework assignment?

    magnitudes = [
        a.plus(b).magnitude() for a in snail_numbers for b in snail_numbers if a != b
    ]

    # Correct answer is 4680!!!!!
    print(f'Part 2: maximum magnitude of a sum is {max(magnitudes)}')
