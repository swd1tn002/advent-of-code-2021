
import os
import sys
from typing import List, Dict, Set
from collections import namedtuple
from queue import PriorityQueue

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

Coord = namedtuple('Coord', 'x y')
Grid = Dict[Coord, int]


def read_puzzle_input(filename=INPUT_FILE) -> Grid:
    """
    The shape of the cavern resembles a square; a quick scan of chiton
    density produces a map of risk level throughout the cave (your puzzle input).
    """
    with open(filename) as file:
        return parse_risk_levels(file.read().split('\n'))


def parse_risk_levels(input: List[str]) -> Grid:
    """
    The number at each position is its risk level.
    ["12", "65"] =>  { Coord(x=0, y=0): 1, Coord(x=1, y=0): 2, Coord(x=0, y=1): 6, Coord(x=1, y=1): 5 }
    """
    rows_and_cols = [line_to_ints(line) for line in input]
    return {Coord(x, y): value for (y, row) in enumerate(rows_and_cols) for (x, value) in enumerate(row)}


def line_to_ints(line: str) -> List[int]:
    """
    Converts string with digits into a list of single digit ints. "123" -> [1, 2, 3]
    """
    return [int(c) for c in line.strip()]


def find_neighbors(grid: Grid, coord: Coord) -> Set[Coord]:
    """
    Get adjacent coordinates not including ones that are diagonally adjacent.
    """
    x, y = coord
    neighbors = ((x-1, y), (x+1, y), (x, y-1), (x, y+1))
    return {Coord(_x, _y) for _x, _y in neighbors if (_x, _y) in grid and coord != (_x, _y)}


# https://stackabuse.com/dijkstras-algorithm-in-python/
def dijkstra(grid: Grid) -> Grid:
    """
    You start in the top left position, your destination is the bottom right position, and you cannot 
    move diagonally. The number at each position is its risk level; to determine the total risk of an
    entire path, add up the risk levels of each position you enter.
    """
    start = Coord(0, 0)

    risk_levels = {**{coord: sys.maxsize for coord in grid.keys()},
                   **{start: 0}}

    queue = PriorityQueue()
    queue.put((0, start))

    visited = set()

    while not queue.empty():
        current_risk, coord = queue.get()
        visited.add(coord)

        for neighbor in (find_neighbors(grid, coord) - visited):
            risk = grid.get(neighbor)

            old_risk = risk_levels.get(neighbor)
            new_risk = current_risk + risk

            if new_risk < old_risk:
                queue.put((new_risk, neighbor))
                risk_levels[neighbor] = new_risk

    return risk_levels


def print_grid(grid: Grid) -> None:
    w = max(c.x for c in grid.keys())
    h = max(c.y for c in grid.keys())

    for y in range(h+1):
        for x in range(w+1):
            print(f'{grid[Coord(x, y)]:1d}', end='')
        print('')
    print('')


def expand_grid(grid: Grid, scale: int) -> Grid:
    """
    The entire cave is actually five times larger in both dimensions than you thought;
    the area you originally scanned is just one tile in a 5x5 tile area that forms the
    full map. Your original map tile repeats to the right and downward; each time the
    tile repeats to the right or downward, all of its risk levels are 1 higher than the
    tile immediately up or left of it.
    """
    vertically_expanded = _expand_vertical(grid, scale)
    return _expand_horizontal(vertically_expanded, scale)


def _expand_horizontal(grid: Grid, scale: int) -> Grid:
    width = max(c.x for c in grid.keys()) + 1
    new_grid = {}

    for coord in grid.keys():
        for i in range(scale):
            offset_x = i * width
            new_coord = Coord(coord.x + offset_x, coord.y)
            new_grid[new_coord] = risk_to_range(grid[coord] + i)
    return new_grid


def _expand_vertical(grid: Grid, scale: int) -> Grid:
    height = max(c.y for c in grid.keys()) + 1
    new_grid = {}

    for coord in grid.keys():
        for i in range(scale):
            offset_y = i * height
            new_coord = Coord(coord.x, coord.y + offset_y)
            new_grid[new_coord] = risk_to_range(grid[coord] + i)
    return new_grid


def risk_to_range(risk: int) -> int:
    """
    Risk levels above 9 wrap back around to 1.
    """
    return risk if risk <= 9 else 1 + risk % 10


if __name__ == '__main__':
    # Part 1
    grid = read_puzzle_input()
    print_grid(grid)

    # Part 1:
    lowest_risk_paths = dijkstra(grid)

    w1 = max(c.x for c in grid.keys())
    h2 = max(c.y for c in grid.keys())
    print(f'Part 1: lowest risk is {lowest_risk_paths[Coord(w1, h2)]}')

    # Part 2:
    expanded = expand_grid(grid, 5)
    lowest_expanded_risks = dijkstra(expanded)

    w2 = max(c.x for c in expanded.keys())
    h2 = max(c.y for c in expanded.keys())
    print(f'Part 2: lowest risk is {lowest_expanded_risks[Coord(w2, h2)]}')
