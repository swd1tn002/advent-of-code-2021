from hydrothermal_vents import parse_coordinate, count_dangerous_points, filter_straight_lines, interpolate_line, create_ocean_floor, parse_line, read_coordinate_file, move_towards, Point
import os


def test_parse_coordinate():
    coord = parse_coordinate('967,44')
    assert coord == (967, 44)


def test_parse_line():
    line = parse_line('372,15 -> 925,568')
    assert line == ((372, 15), (925, 568))


def test_read_coordinate_file():
    lines = read_coordinate_file()

    assert lines[0] == ((445, 187), (912, 654))
    assert lines[-1] == ((727, 365), (727, 216))


def test_filter_straight_lines():
    straight = parse_line('372,15 -> 925,15')
    not_straight = parse_line('372,20 -> 925,15')

    assert filter_straight_lines([straight, not_straight]) == [straight]


def test_move_towards():
    start = parse_coordinate('10,10')
    end = parse_coordinate('0,20')

    next = move_towards(start, end)

    assert next.x == 9
    assert next.y == 11


def test_interpolate_line():
    line = parse_line('0, 9 -> 5, 9')
    points = interpolate_line(line)

    assert points == [Point(0, 9), Point(
        1, 9), Point(2, 9), Point(3, 9), Point(4, 9), Point(5, 9)]


def test_create_ocean_floor():
    line1 = parse_line('0,0 -> 10,0')
    line2 = parse_line('5,0 -> 5,10')

    floor = create_ocean_floor([line1, line2])

    assert floor[Point(0, 0)] == 1
    assert floor[Point(5, 0)] == 2
    assert count_dangerous_points(floor) == 1


def test_aoc_test_input():
    file = os.path.join(os.path.dirname(__file__), 'test_input.txt')

    lines = read_coordinate_file(file)
    straight = filter_straight_lines(lines)

    floor = create_ocean_floor(straight)
    assert count_dangerous_points(floor) == 5
