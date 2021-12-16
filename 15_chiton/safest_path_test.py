from safest_path import *


def test_read_puzzle_input():
    grid = read_puzzle_input()

    assert grid[Coord(0, 0)] == 9
    assert grid[Coord(1, 1)] == 1


def test_find_neighbors():
    grid = read_puzzle_input()

    neighbors = find_neighbors(grid, Coord(5, 10))

    assert neighbors == {Coord(4, 10), Coord(6, 10), Coord(5, 9), Coord(5, 11)}


def test_find_lowest_risks():
    grid = {
        Coord(0, 0): 1,
        Coord(1, 0): 2,
        Coord(0, 1): 3,
        Coord(1, 1): 4
    }

    costs = find_lowest_risks(grid)

    assert costs[Coord(0, 0)] == 0
    assert costs[Coord(1, 0)] == 2
    assert costs[Coord(0, 1)] == 3
    assert costs[Coord(1, 1)] == 6


def test_expand_grid():
    grid = {
        Coord(0, 0): 1,
        Coord(1, 0): 2,
        Coord(0, 1): 3,
        Coord(1, 1): 9
    }

    expanded = expand_grid(grid, 2)

    assert len(expanded) == 4 * len(grid)

    assert expanded[Coord(2, 0)] == 2  # incremented by 1
    assert expanded[Coord(1, 3)] == 1  # 10 wraps over to 1
