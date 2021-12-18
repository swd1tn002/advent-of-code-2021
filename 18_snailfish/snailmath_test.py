from snailmath import *


def test_reading_input():
    lines = read_puzzle_input()

    assert lines[0] == '[[[6,[8,3]],[2,0]],[[[9,5],[9,1]],3]]'
    assert lines[-1] == '[9,6]'


def test_parse_snailmath():
    pair = parse('[[3,4],5]')

    assert pair.left.left.value == 3
    assert pair.left.right.value == 4
    assert pair.right.value == 5


def test_addition():
    l = Pair(Value(1), Value(2))
    r = Pair(Pair(Value(3), Value(4)), Value(5))
    result = l.plus(r)
    assert result == Pair(l, r)


def test_exploding_formulas():
    # Examples from https://adventofcode.com/2021/day/18
    num = parse('[[[[[9,8],1],2],3],4]')._reduce()
    assert repr(num) == '[[[[0,9],2],3],4]'

    num = parse('[7,[6,[5,[4,[3,2]]]]]')._reduce()
    assert repr(num) == '[7,[6,[5,[7,0]]]]'

    num = parse('[[6,[5,[4,[3,2]]]],1]')._reduce()
    assert repr(num) == '[[6,[5,[7,0]]],3]'


def test_addition_with_splits():
    n1 = parse('[[[[4,3],4],4],[7,[[8,4],9]]]')
    n2 = parse('[1,1]')

    assert repr(n1.plus(n2)) == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'


def test_magnitude():
    mag = parse('[[1,2],[[3,4],5]]')
    assert mag.magnitude() == 143


def test_sum_and_magnitude():
    m1 = parse('[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]')
    m2 = parse('[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]')
    assert m1.plus(m2).magnitude() == 3993


def test_total_magnitude():
    puzzle_input = read_puzzle_input()

    snail_numbers = [parse(line) for line in puzzle_input]

    snail = snail_numbers[0]
    for next_num in snail_numbers[1:]:
        snail = snail.plus(next_num)

    assert snail.magnitude() == 3411


def test_max_magnitude_pair():
    puzzle_input = read_puzzle_input()
    snail_numbers = [parse(line) for line in puzzle_input]

    magnitudes = [
        a.plus(b).magnitude() for a in snail_numbers for b in snail_numbers if a != b
    ]

    assert max(magnitudes) == 4680
