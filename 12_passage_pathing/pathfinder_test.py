from pathfinder import *
from pytest import fixture


@fixture
def test_caves():
    return ['start-A',
            'start-b',
            'A-c',
            'A-b',
            'b-d',
            'A-end',
            'b-end']


def test_reading_input_file():
    lines = read_input_file()

    assert lines[0] == 'end-MY'
    assert lines[-1] == 'start-NF'


def test_build_cave_system_returns_the_start_cave(test_caves):
    start = build_cave_system(test_caves)

    assert start.is_start()
    assert len(start.get_routes()) == 2


def test_find_routes(test_caves):
    """
    ...given these rules, there are 10 paths through this example cave system.
    """
    start = build_cave_system(test_caves)
    routes = find_routes(start)

    assert len(routes) == 10


def test_find_routes_part2(test_caves):
    """
    Now, there are 36 possible paths through the first example.
    """
    start = build_cave_system(test_caves)
    routes = find_routes_part2(start)

    assert len(routes) == 36
