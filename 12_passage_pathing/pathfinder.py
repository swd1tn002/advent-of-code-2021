"""
With your submarine's subterranean subsystems subsisting suboptimally, the only way you're getting 
out of this cave anytime soon is by finding a path yourself. Not just a path - the only way to know
if you've found the best path is to find all of them.
"""

from __future__ import annotations
import os
from typing import List, Dict

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


class Cave:
    def __init__(self, name) -> None:
        self.name: str = name
        self.routes: List[Cave] = []

    def add_route(self, next: Cave):
        self.routes.append(next)

    def get_routes(self) -> List[Cave]:
        return list(self.routes)

    def is_big(self) -> bool:
        """
        There are two types of caves: big caves (written in uppercase, like A) and small caves (written in lowercase, like b).
        """
        return self.name == self.name.upper()

    def is_small(self) -> bool:
        """
        There are two types of caves: big caves (written in uppercase, like A) and small caves (written in lowercase, like b).
        """
        return not self.is_big()

    def is_start(self) -> bool:
        return self.name == 'start'

    def is_end(self) -> bool:
        return self.name == 'end'

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)


def read_input_file() -> List[str]:
    """
    Fortunately, the sensors are still mostly working, and so you build a 
    rough map of the remaining caves (your puzzle input).
    This is a list of how all of the caves are connected. You start in the cave 
    named start, and your destination is the cave named end. An entry like b-d
    means that cave b is connected to cave d - that is, you can move between them.
    """
    with open(INPUT_FILE) as file:
        return file.read().split('\n')


def build_cave_system(input: List[str]) -> Cave:
    """
    Input is a list of how all of the caves are connected. You start in the cave named 
    start, and your destination is the cave named end. An entry like b-d means that 
    cave b is connected to cave d - that is, you can move between them.
    """
    caves: Dict[str, Cave] = dict()

    for line in input:
        point_a, point_b = line.split('-')
        cave_a = caves.get(point_a, Cave(point_a))
        cave_b = caves.get(point_b, Cave(point_b))

        cave_a.add_route(cave_b)
        cave_b.add_route(cave_a)

        caves[point_a] = cave_a
        caves[point_b] = cave_b

    return caves['start']


def find_routes(current: Cave, path: List[Cave] = [], complete: List[List[Cave]] = []) -> List[List[Cave]]:
    """
    Your goal is to find the number of distinct paths that start at start, end at end, and don't 
    visit small caves more than once. It would be a waste of time to visit any small cave more than once,
    but big caves are large enough that it might be worth visiting them multiple times. So, all paths 
    you find should visit small caves at most once, and can visit big caves any number of times.
    """
    new_path = [*path, current]

    if current.is_end():
        # Found a path to end
        complete.append(new_path)
        return complete

    for next_cave in current.get_routes():
        if next_cave.is_big() or next_cave not in new_path:
            find_routes(next_cave, new_path, complete)

    return complete


def find_routes_part2(current: Cave, path: List[Cave] = [], complete: List[List[Cave]] = []) -> List[List[Cave]]:
    """
    After reviewing the available paths, you realize you might have time to visit a single small
    cave twice. Specifically, big caves can be visited any number of times, a single small cave
    can be visited at most twice, and the remaining small caves can be visited at most once.
    """
    new_path = [*path, current]

    if current.is_end():
        # Found a path to end
        complete.append(new_path)
        return complete

    for next_cave in current.get_routes():
        # start and end can only be visited exactly once each
        if next_cave.is_start():
            continue

        elif next_cave.is_big():
            complete = find_routes_part2(next_cave, new_path, complete)

        # is small cave
        elif (next_cave not in new_path) or (not visited_any_small_cave_twice(new_path)):
            complete = find_routes_part2(next_cave, new_path, complete)

    return complete


def visited_any_small_cave_twice(path: List[Cave]) -> bool:
    return any(path.count(cave) > 1 for cave in path if cave.is_small())


if __name__ == '__main__':
    caves = read_input_file()
    start = build_cave_system(caves)

    # Part 1:
    routes_1 = find_routes(start)
    print(f'Part 1: {len(routes_1)}')

    # Part 2:
    routes_2 = find_routes_part2(start)
    print(f'Part 2: {len(routes_2)}')
