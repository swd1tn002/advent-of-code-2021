import os
from typing import List, Dict, Set
from collections import namedtuple

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

Coord = namedtuple('Coord', 'x y')


def read_heightmap(filename=INPUT_FILE) -> Dict[Coord, int]:
    """
    The submarine generates a heightmap of the floor of
    the nearby caves for you (your puzzle input).
    """
    with open(filename) as file:
        return parse_heightmap(file.readlines())


def parse_heightmap(input: List[str]) -> Dict[Coord, int]:
    """
    Parses the given list of strings into a dict with the x and y axis coordinates as
    keys and respective numbers as values:
    ["12", "65"] =>  { Coord(x=0, y=0): 1, Coord(x=1, y=0): 2, Coord(x=0, y=1): 6, Coord(x=1, y=1): 5 }
    """
    rows_and_cols = list(map(line_to_ints, input))
    return {Coord(x, y): value for (y, row) in enumerate(rows_and_cols) for (x, value) in enumerate(row)}


def line_to_ints(line: str) -> List[int]:
    """
    Converts string with digits into a list of single digit ints.
    """
    return list(map(int, line.strip()))


def find_neighbors(heightmap: Dict[Coord, int], coord: Coord) -> Set[Coord]:
    """
    Most locations have four adjacent locations (up, down, left, and right); 
    locations on the edge or corner of the map have three or two adjacent locations,
    respectively. (Diagonal locations do not count as adjacent.)
    """
    x, y = coord
    return {Coord(_x, _y) for (_x, _y) in ((x, y-1), (x, y+1), (x-1, y), (x+1, y)) if (_x, _y) in heightmap}


def find_basins(heightmap: Dict[Coord, int], points: List[Coord]) -> List[List[Coord]]:
    return [find_basin(heightmap, coord) for coord in points]


def find_basin(heightmap: Dict[Coord, int], point: Coord) -> Set[Coord]:
    """
    A basin is all locations that eventually flow downward to a single low point. Therefore,
    every low point has a basin, although some basins are very small. Locations of height 9
    do not count as being in any basin, and all other locations will always be part of 
    exactly one basin.
    """
    visited = set()
    queue = [point]

    while len(queue) > 0:
        next = queue.pop(0)

        visited.add(next)
        queue += [n for n in find_neighbors(heightmap, next)
                  if heightmap[n] != 9 and n not in {*visited, * queue}]

    return visited


def find_low_points(heightmap: Dict[Coord, int]) -> List[Coord]:
    """
    Your first goal is to find the low points - the locations that are lower than any 
    of its adjacent locations.
    """
    low_points = []

    # Your first goal is to find the low points - the locations that are lower than any of its adjacent locations.
    for coord, value in heightmap.items():
        adjacent_values = [heightmap[n]
                           for n in find_neighbors(heightmap, coord)]
        if all(value < neighbour for neighbour in adjacent_values):
            low_points.append(coord)

    return low_points


if __name__ == '__main__':
    heightmap = read_heightmap()

    low_points = find_low_points(heightmap)

    print(f'Low points: {low_points}')

    # Part 1: What is the sum of the risk levels of all low points on your heightmap?
    # The risk level of a low point is 1 plus its height
    risk_levels = sum(1 + heightmap[c] for c in low_points)

    print(f'Risk level: {risk_levels}')

    # Part 2: What do you get if you multiply together the sizes of the three largest basins?
    basins = find_basins(heightmap, low_points)
    basin_sizes = list(map(len, basins))
    basin_sizes.sort()

    print(f'Part 2: {basin_sizes[-3] * basin_sizes[-2] * basin_sizes[-1]}')
