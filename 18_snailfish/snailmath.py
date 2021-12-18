
import re
from typing import Tuple
from collections import namedtuple

Overflow = namedtuple('Overflow', 'left right')


class Pair:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def plus(self, other: 'Pair') -> 'Pair':
        return Pair(self, other)

    def __repr__(self) -> str:
        return f'[{self.left},{self.right}]'

    def reduce(self) -> bool:
        while self.explode(1)[0] or self.split():
            continue
        return self

    def explode(self, depth) -> Tuple:
        if depth == 4:
            if self.left.can_explode():
                # the pair's right value is added to the first regular number to the right of the exploding pair(if any)
                self.right.add_left(self.left.right.value)

                overflow = self.left.left
                self.left = Value(0)
                # exploded with overflowing left value
                return True, Overflow(overflow, None)
            elif self.right.can_explode():
                # the pair's left value is added to the first regular number to the left of the exploding pair
                self.left.add_right(self.right.left.value)
                overflow = self.right.right
                self.right = Value(0)
                # exploded with overflowing right value
                return True, Overflow(None, overflow)
            return False, Overflow(None, None)  # not exploded
        else:
            exploded_left, overflow = self.left.explode(depth + 1)

            if exploded_left:
                if overflow.left:
                    return True, overflow  # Could not apply overflow here

                if overflow.right:
                    self.right.add_left(overflow.right.value)

                return True, Overflow(None, None)

            exploded_right, overflow = self.right.explode(depth + 1)

            if exploded_right:
                if overflow.right:
                    return True, overflow  # Could not apply overflow here

                if overflow.left:
                    self.left.add_right(overflow.left.value)

                return True, Overflow(None, None)

            return exploded_left or exploded_right, Overflow(None, None)

    def can_explode(self) -> bool:
        return True

    def can_split(self) -> bool:
        return self.left.can_split() or self.right.can_split()

    def split(self) -> bool:
        if self.left.can_split():
            self.left = self.left.split()
            return self
        elif self.right.can_split():
            self.right = self.right.split()
            return self
        return None

    def add_right(self, value):
        self.right.add_right(value)

    def add_left(self, value):
        self.left.add_left(value)

    def magnitude(self) -> int:
        """
        The magnitude of a pair is 3 times the magnitude of its left element plus 2 times the magnitude 
        of its right element.
        """
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()


class Value(Pair):
    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        return f'{self.value}'

    def explode(self, depth):
        return False, Overflow(None, None)

    def can_explode(self) -> bool:
        return False

    def add_right(self, value):
        self.value += value

    def add_left(self, value):
        self.value += value

    def can_split(self) -> bool:
        return self.value >= 10

    def split(self) -> Pair:
        return Pair(Value(self.value // 2), Value((self.value + 1) // 2))

    def magnitude(self) -> int:
        """
        The magnitude of a regular number is just that number.
        """
        return self.value


l = Pair(Value(1), Value(2))
r = Pair(Pair(Value(3), Value(4)), Value(5))

result = l.plus(r)
print(result)


def parse_snailfish_number(formula: str) -> Pair:
    """
    [1,2] => Pair(Value(1), Value(2))
    [[3,4],5] => Pair(Pair(Value(3), Value(4)), Value(5))
    """
    formula = re.sub(r'[^\d\[\],]', '', formula)  # Clean up anything extra
    formula = re.sub(r'(\d)', r'Value(\1)', formula)
    return eval(formula.replace('[', 'Pair(').replace(']', ')'))


# Test parsing
parsed = parse_snailfish_number('[[3,4],5]')
print(parsed)


def test_exploding(formula, expected):
    snailnum = parse_snailfish_number(formula)
    snailnum.explode(1)
    print(f'{formula} => {snailnum}')
    print(f'{repr(snailnum) == expected}')  # Success?
    print()


test_exploding('[[[[[9,8],1],2],3],4]', '[[[[0,9],2],3],4]')
test_exploding('[7,[6,[5,[4,[3,2]]]]]', '[7,[6,[5,[7,0]]]]')
test_exploding('[[6,[5,[4,[3,2]]]],1]', '[[6,[5,[7,0]]],3]')
test_exploding('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]',
               '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')

# Test reducing with splits
n1 = parse_snailfish_number('[[[[4,3],4],4],[7,[[8,4],9]]]')
n2 = parse_snailfish_number('[1,1]')

result = n1.plus(n2)
print(result.reduce())


# Test magnitude
mag = parse_snailfish_number('[[1,2],[[3,4],5]]')
print(f'Magnitude is {mag.magnitude()}, {mag.magnitude() == 143}')

puzzle_input = """[[[6,[8,3]],[2,0]],[[[9,5],[9,1]],3]]
[[[9,[2,2]],[5,4]],[[[2,2],[9,6]],[7,7]]]
[[[0,[3,2]],1],[[0,[2,8]],[2,[0,4]]]]
[[4,4],[[[7,0],5],[3,1]]]
[[5,4],1]
[[[[7,6],4],9],[[9,1],9]]
[[[1,[7,8]],[[7,7],[1,6]]],[1,[6,[7,1]]]]
[[[[6,8],[5,6]],[[1,1],8]],[[[2,0],[3,1]],[2,[2,6]]]]
[[[6,3],[3,[7,1]]],8]
[[[9,4],[3,[0,6]]],[[2,[3,6]],[[9,8],[1,6]]]]
[9,[0,[[0,7],2]]]
[[[[8,4],7],[[9,2],[0,9]]],[[7,9],[8,[0,9]]]]
[[1,1],[[5,[3,8]],[3,[4,7]]]]
[[[9,[2,9]],[2,[2,9]]],[[[3,5],5],[[3,3],2]]]
[[[[5,4],9],0],[[[5,7],2],[[5,2],9]]]
[[2,[[1,0],[6,2]]],0]
[[[3,7],[7,6]],[[[2,8],5],[3,[9,7]]]]
[[2,[2,[8,8]]],[[[9,9],[1,1]],[[8,6],[0,3]]]]
[[8,1],[3,5]]
[[7,[[7,6],[2,0]]],4]
[[5,4],[[1,3],[5,[2,8]]]]
[7,9]
[[[[6,9],0],[1,[5,0]]],[[[6,4],3],7]]
[[[[3,7],3],[2,6]],[[0,4],[9,9]]]
[[[[1,5],[5,0]],[9,4]],[[[8,3],3],[8,[3,6]]]]
[[[[3,7],5],[[8,5],[1,5]]],[[0,6],[3,4]]]
[[[[4,0],2],[7,[8,4]]],[0,[5,[7,8]]]]
[[[[0,8],[0,4]],[9,3]],[[[5,4],[4,8]],[[1,6],[5,4]]]]
[[0,[0,3]],[[3,[1,5]],[[9,6],[0,6]]]]
[[9,[8,4]],[7,1]]
[[[[1,9],[7,7]],9],[[6,[4,5]],[8,[3,2]]]]
[5,[[2,[9,5]],[3,[4,0]]]]
[[[6,2],[[1,8],5]],6]
[[8,[6,[6,4]]],[0,[[9,8],7]]]
[[[[6,3],[8,0]],[8,[2,7]]],8]
[[[6,[3,6]],[[4,0],[4,7]]],[0,[[4,0],[4,5]]]]
[[[3,[8,1]],1],[2,3]]
[[[6,[7,0]],[[3,5],[3,4]]],7]
[[[[8,0],3],8],[[[1,6],3],[[0,5],2]]]
[[[3,7],[[9,8],8]],[[[8,4],7],[3,[1,7]]]]
[[[0,5],[[5,5],[7,8]]],[9,[5,[2,2]]]]
[[2,9],[[[7,4],4],[[8,0],[6,9]]]]
[[[[7,8],[8,8]],0],9]
[[[4,[0,6]],[[5,9],[0,1]]],[3,[6,7]]]
[[[7,[6,9]],[5,[6,4]]],[[[3,9],6],[[0,1],1]]]
[3,[[[6,9],7],[5,8]]]
[[[3,9],[[3,5],2]],[[[2,5],[4,6]],[8,0]]]
[[[9,7],3],[[[2,7],[0,9]],[3,[0,3]]]]
[[3,[4,0]],[[6,6],[4,5]]]
[[0,0],[[5,9],1]]
[[[6,8],[2,6]],[[[1,1],3],7]]
[[[4,4],[[1,0],[2,4]]],[2,6]]
[[[[6,0],6],[8,[9,9]]],[[4,2],[[1,8],[5,3]]]]
[[[[1,6],[4,3]],[5,5]],[[7,[9,9]],4]]
[[[[6,9],7],[9,3]],[[[9,6],5],0]]
[[3,[[7,2],[8,1]]],[[7,[3,0]],1]]
[0,[0,[1,3]]]
[[[0,5],[[6,1],[4,6]]],[[[0,4],8],[[4,5],9]]]
[[[[7,5],[7,0]],[6,[7,2]]],[7,[3,[4,1]]]]
[[3,3],[0,[6,2]]]
[[[3,8],[[7,3],6]],[[[0,8],3],[[8,9],[2,9]]]]
[[4,[[5,6],[4,0]]],[[7,[7,5]],[5,0]]]
[[[[2,5],[5,4]],9],[[[6,0],[0,0]],[[5,1],8]]]
[[2,[[1,7],7]],[[[4,5],[7,9]],0]]
[[[0,9],[[5,4],3]],3]
[[9,[[1,9],[1,6]]],[[9,[0,3]],[[8,8],[0,7]]]]
[[[[7,2],4],[7,8]],[[[4,1],[3,1]],[2,5]]]
[[[[1,8],3],[2,5]],[[0,[5,8]],[[1,3],[5,2]]]]
[[3,9],[[9,6],[5,[7,1]]]]
[1,[[3,[6,5]],[5,[2,7]]]]
[[[5,8],6],[8,[[9,4],[0,4]]]]
[0,[[5,[6,6]],[[7,4],[4,6]]]]
[[[[6,8],2],[[1,6],[8,2]]],6]
[7,2]
[[3,1],7]
[[[2,[9,5]],0],[[[7,3],4],8]]
[[[[0,0],[4,2]],5],[[8,6],2]]
[[1,[7,8]],[2,[[6,6],[5,7]]]]
[[[3,[6,0]],3],[[7,[4,4]],8]]
[[[9,[8,7]],[[4,2],4]],[[6,1],[[3,3],[2,2]]]]
[[[8,1],[[7,4],[5,9]]],9]
[[[2,[8,6]],[[9,8],2]],[[9,5],[1,[9,8]]]]
[[[[6,1],[3,1]],[[4,5],1]],[[[6,4],[6,2]],2]]
[[[[4,0],[0,1]],[[1,4],6]],7]
[[[[8,9],[0,2]],4],[[[9,8],8],[0,[0,6]]]]
[0,[[[0,9],1],7]]
[[1,[[3,7],3]],[[[2,4],3],0]]
[[[[7,6],3],8],[[5,5],9]]
[[2,[1,3]],[[[6,7],3],[[3,8],7]]]
[[[[0,6],6],6],[[5,[0,9]],[8,[2,4]]]]
[4,[[[3,0],[2,5]],[[7,4],1]]]
[[[[7,9],3],[0,[8,2]]],[[8,[3,4]],[[2,3],[1,6]]]]
[[[3,[6,3]],5],[[3,4],2]]
[[[[1,9],[0,3]],[0,8]],[[[4,2],[4,3]],[[8,9],5]]]
[[[[2,8],[4,9]],[[3,5],6]],[[6,[1,5]],[0,[9,7]]]]
[[6,3],[[[7,7],[1,7]],[[6,5],[0,8]]]]
[[1,[1,[5,8]]],7]
[[0,6],[9,[[3,4],0]]]
[[[[0,2],7],9],9]
[9,6]""".split('\n')

test_puzzle_input = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""".split('\n')

snail_numbers = [parse_snailfish_number(line)
                 for line in puzzle_input]

snail = snail_numbers[0]
for next_num in snail_numbers[1:]:
    snail = snail.plus(next_num).reduce()

print(snail.magnitude())

magnitudes = [
    parse_snailfish_number(a).plus(parse_snailfish_number(b)).reduce().magnitude() for a in puzzle_input for b in puzzle_input if a != b
]

print(max(magnitudes))  # Correct answer is 4680!!!!!
# 2370 is too low
# 1706 is too low


# Testing with example
m1 = parse_snailfish_number('[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]')
m2 = parse_snailfish_number(
    '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]')

print(m1.plus(m2).reduce().magnitude())
