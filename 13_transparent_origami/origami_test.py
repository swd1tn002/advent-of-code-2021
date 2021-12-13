from origami import *

# example from https://adventofcode.com/2021/day/13
TEST_LINES = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5""".split('\n')


def test_read_puzzle_input():
    data = read_puzzle_input()
    assert data[0] == '428,532'
    assert data[-1] == 'fold along y=6'


def test_parse_points():
    points = parse_points(TEST_LINES)

    assert len(points) == 18
    assert Point(6, 10) in points
    assert Point(2, 14) in points


def test_parse_folds():
    folds = parse_folds(TEST_LINES)

    assert folds == [Fold('y', 7), Fold('x', 5)]


def test_apply_fold_point_below_fold_line():
    folded_up = apply_fold(Point(0, 14), Fold('y', 7))
    assert folded_up == Point(0, 0)


def test_apply_fold_point_below_fold_line():
    not_folded = apply_fold(Point(2, 2), Fold('y', 7))
    assert not_folded == Point(2, 2)


def test_apply_fold_point_below_fold_line():
    folded_left = apply_fold(Point(14, 0), Fold('x', 7))
    assert folded_left == Point(0, 0)


def test_apply_fold_point_below_fold_line():
    not_folded = apply_fold(Point(2, 2), Fold('x', 7))
    assert not_folded == Point(2, 2)
