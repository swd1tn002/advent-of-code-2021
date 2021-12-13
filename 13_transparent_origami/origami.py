import os
from typing import List
from collections import namedtuple

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

Point = namedtuple('Point', 'x y')
Fold = namedtuple('Fold', 'axis position')


def read_puzzle_input(filename=INPUT_FILE) -> List[str]:
    """
    Each octopus has an energy level - your submarine can remotely measure 
    the energy level of each octopus (your puzzle input)
    """
    with open(filename) as file:
        return file.read().split('\n')


def parse_points(lines: List[str]) -> List[Point]:
    """
    The transparent paper is marked with random dots and includes
    instructions on how to fold it up (your puzzle input).
    The first section is a list of dots on the transparent paper. 
    0,0 represents the top-left coordinate.
    """
    points = set()
    point_lines = [l for l in lines if 'fold' not in l and l != '']

    for line in point_lines:
        x, y = line.split(',')
        point = Point(int(x), int(y))
        points.add(point)
    return points


def parse_folds(lines: List[str]) -> List[Fold]:
    """
    Then, there is a list of fold instructions. Each instruction indicates a
    line on the transparent paper and wants you to fold the paper up
    (for horizontal y=... lines) or left (for vertical x=... lines).
    """
    folds = []
    fold_lines = [l for l in lines if 'fold' in l]
    for fold in fold_lines:
        fold = fold.replace('fold along ', '')
        axis, position = fold.split('=')
        folds.append(Fold(axis, int(position)))
    return folds


def apply_fold(point: Point, fold: Fold) -> Point:
    """
    Each instruction indicates a line on the transparent paper and wants you to
    fold the paper up (for horizontal y=... lines) or left (for vertical x=... lines).
    """
    if fold.axis == 'x':
        return fold_left(point, fold.position)
    else:
        return fold_up(point, fold.position)


def fold_left(point: Point, x: int):
    """
    Folds the given point to the left, if it is on the right side of the fold  line.
    """
    if point.x <= x:
        return point
    else:
        return Point(x-(point.x - x), point.y)


def fold_up(point: Point, y: int):
    """
    Folds the given point up, if it is below the fold line.
    """
    if point.y <= y:
        return point
    else:
        return Point(point.x, y - (point.y - y))


def print_points(points: List[Point]):
    """
    Prints the coordinates in this example form in a pattern, where # is a dot on the paper
    and others are empty, unmarked positions.
    """
    width = max(p.x for p in points) + 1
    height = max(p.y for p in points) + 1

    for y in range(height):
        for x in range(width):
            if Point(x, y) in points:
                print('#', end='')
            else:
                print(' ', end='')
        print()
    print()


if __name__ == '__main__':
    data = read_puzzle_input()
    points = parse_points(data)
    folds = parse_folds(data)

    # Part 1
    first_fold = folds[0]
    part1 = {apply_fold(point, first_fold) for point in points}
    print(f'Part 1: {len(part1)}')

    # Part 2
    for fold in folds:
        points = {apply_fold(point, fold) for point in points}

    print('Part 2:')
    print_points(points)
