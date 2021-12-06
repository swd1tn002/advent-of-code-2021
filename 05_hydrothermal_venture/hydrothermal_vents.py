from typing import List, Tuple, Dict
from collections import namedtuple
import os
INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

Point = namedtuple('Point', 'x y')
Line = namedtuple('Line', 'start end')


def read_coordinate_file(filename=INPUT_FILE) -> List[Line]:
    """
    Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 
    where x1,y1 are the coordinates of one end the line segment and x2,y2 are
    the coordinates of the other end. These line segments include the points
    at both ends.
    """
    with open(filename) as file:
        lines = file.read().splitlines()

    return list(map(parse_line, lines))


def parse_line(input: str) -> Line:
    """
    Takes a string of two points ('1,2 -> 1,3') and returns a Line between the points.
    """
    p1, p2 = map(parse_coordinate, input.split(' -> '))
    return Line(p1, p2)


def parse_coordinate(point: str) -> Point:
    """
    Takes a str such as '1,2' and returns a Point(1, 2)
    """
    x, y = map(int, point.split(','))
    return Point(x, y)


def filter_straight_lines(lines: List[Line]):
    """
    Only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.
    """
    return list(filter(lambda l: l.start.x == l.end.x or l.start.y == l.end.y, lines))


def interpolate_line(line: Line) -> List[Point]:
    """
    Creates a list of neighbouring points from line start to line end.
    """
    points = [line.start]
    while points[-1] != line.end:
        points.append(move_towards(points[-1], line.end))

    return points


def move_towards(point: Point, target: Point) -> Point:
    """
    Creates a new Point which is one step closer to the target point on both x and y axis.
    """
    def max_one(num): return num / abs(num) if num != 0 else 0

    x_step = max_one(target.x - point.x)
    y_step = max_one(target.y - point.y)

    return Point(point.x + x_step, point.y + y_step)


def create_ocean_floor(lines: List[Line]) -> Dict:
    """
    Creates a dictionary with Points as keys and the number of lines
    passing the point as values.
    """
    floor = {}
    for line in lines:
        points = interpolate_line(line)
        for point in points:
            floor[point] = floor.get(point, 0) + 1
    return floor


def count_dangerous_points(ocean_floor: dict) -> int:
    """
    Determines the number of points where at least two lines overlap.
    """
    return len([num for num in ocean_floor.values() if num > 1])


if __name__ == '__main__':
    all_lines = read_coordinate_file()
    straight_lines = filter_straight_lines(all_lines)

    floor_challenge_1 = create_ocean_floor(straight_lines)
    danger_1 = count_dangerous_points(floor_challenge_1)
    print(f'Dangerous positions in challenge 1: {danger_1}')

    floor_challenge_2 = create_ocean_floor(all_lines)
    danger_2 = count_dangerous_points(floor_challenge_2)
    print(f'Dangerous positions in challenge 2: {danger_2}')
