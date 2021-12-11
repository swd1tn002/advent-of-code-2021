from octopus import *


input = ['11111',
         '19991',
         '19191',
         '19991',
         '11111']


def test_parsing_input():
    grid = parse_energy_levels(input)

    assert grid[Coord(0, 0)] == 1
    assert grid[Coord(1, 1)] == 9


def test_find_neighbors():
    grid = parse_energy_levels(input)
    neighbors = find_neighbors(grid, (Coord(0, 0)))

    assert len(neighbors) == 3
    assert Coord(1, 1) in neighbors
    assert Coord(0, 0) not in neighbors


def test_next_step():
    # From https://adventofcode.com/2021/day/11 example
    grid = parse_energy_levels(input)

    next_grid, flashes = next_step(grid)

    expected = parse_energy_levels(['34543',
                                    '40004',
                                    '50005',
                                    '40004',
                                    '34543'])
    assert next_grid == expected
    assert flashes == 9
