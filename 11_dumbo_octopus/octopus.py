
import os
from typing import List, Dict, Set, Tuple
from collections import namedtuple

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

Coord = namedtuple('Coord', 'x y')


def read_energy_levels(filename=INPUT_FILE) -> Dict[Coord, int]:
    """
    Each octopus has an energy level - your submarine can remotely measure 
    the energy level of each octopus (your puzzle input)
    """
    with open(filename) as file:
        return parse_energy_levels(file.readlines())


def parse_energy_levels(input: List[str]) -> Dict[Coord, int]:
    """
    Parses the given list of strings into a dict with the x and y axis coordinates as
    keys and respective numbers as values:
    ["12", "65"] =>  { Coord(x=0, y=0): 1, Coord(x=1, y=0): 2, Coord(x=0, y=1): 6, Coord(x=1, y=1): 5 }
    """
    rows_and_cols = [line_to_ints(line) for line in input]
    return {Coord(x, y): value for (y, row) in enumerate(rows_and_cols) for (x, value) in enumerate(row)}


def line_to_ints(line: str) -> List[int]:
    """
    Converts string with digits into a list of single digit ints.
    """
    return list(map(int, line.strip()))


def find_neighbors(grid: Dict[Coord, int], coord: Coord) -> Set[Coord]:
    """
    Get adjacent coordinates including ones that are diagonally adjacent.
    """
    x, y = coord
    return {Coord(_x, _y) for _x in range(x-1, x+2) for _y in range(y-1, y+2) if (_x, _y) in grid and coord != (_x, _y)}


def next_step(grid: Dict[Coord, int]) -> Tuple[Dict[Coord, int], int]:
    # First, the energy level of each octopus increases by 1.
    new_grid = {c: level+1 for c, level in grid.items()}

    # Then, any octopus with an energy level greater than 9 flashes. This increases
    # the energy level of all adjacent octopuses by 1, including octopuses that are diagonally adjacent.
    # If this causes an octopus to have an energy level greater than 9, it also flashes. This process
    # continues as long as new octopuses keep having their energy level increased beyond 9.
    flashed = set()
    while any(level > 9 and coord not in flashed for coord, level in new_grid.items()):
        flashing = {
            coord for coord, value in new_grid.items() if value > 9 and coord not in flashed
        }
        for flash in flashing:
            for neighbor in find_neighbors(new_grid, flash):
                new_grid[neighbor] += 1

        flashed = flashed | flashing

    # Finally, any octopus that flashed during this step has its energy level set to 0, as it used
    # all of its energy to flash.
    return {c: level if level <= 9 else 0 for c, level in new_grid.items()}, len(flashed)


def print_grid(grid: Dict[Coord, int]) -> None:
    w = max(c.x for c in grid.keys()) + 1
    h = max(c.y for c in grid.keys()) + 1

    for y in range(h):
        for x in range(w):
            print(grid[Coord(x, y)], end='')
        print('')
    print('')


if __name__ == '__main__':
    # Part 1
    grid = read_energy_levels()
    flashes = 0
    for i in range(100):
        grid, flashed = next_step(grid)
        flashes += flashed

    print_grid(grid)

    print(f'Part 1: flashed {flashes} times')

    # Part 2
    grid = read_energy_levels()
    for i in range(1, 1_000):
        grid, flashed = next_step(grid)
        if all(value == 0 for value in grid.values()):
            print(f'Part 2: Synchronized after {i} steps!')
            break
