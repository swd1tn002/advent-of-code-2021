import os
from typing import List, Dict
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
    heightmap = dict()
    rows_and_cols = list(map(line_to_ints, input))

    for y, row in enumerate(rows_and_cols):
        for x, value in enumerate(row):
            heightmap[Coord(x, y)] = value
    return heightmap


def line_to_ints(line: str) -> List[int]:
    return list(map(int, line.strip()))


def find_neighbors(heightmap: Dict[Coord, int], coord: Coord) -> List[int]:
    neighbors = [
        Coord(coord.x, coord.y - 1),
        Coord(coord.x, coord.y + 1),
        Coord(coord.x - 1, coord.y),
        Coord(coord.x + 1, coord.y)
    ]

    return [heightmap[c] for c in neighbors if c in heightmap]


if __name__ == '__main__':
    heightmap = read_heightmap()
    print(heightmap)

    height = max(coord.y for coord in heightmap.keys()) + 1
    width = max(coord.x for coord in heightmap.keys()) + 1

    risk_levels = []
    low_points = []

    for coord in heightmap.keys():
        value = heightmap[coord]
        neighbours = find_neighbors(heightmap, coord)
        if all(value < neighbour for neighbour in neighbours):
            low_points.append(coord)
            risk_levels.append(value + 1)

    print(f'Low points: {low_points}')
    print(f'Risk level: {sum(risk_levels)}')
