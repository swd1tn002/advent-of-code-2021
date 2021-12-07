from collections import namedtuple
import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

Command = namedtuple('Command', 'direction amount')


def parse_line(line):
    direction, amount = line.split(' ')
    return Command(direction, int(amount))


def read_course_file():
    """The submarine seems to already have a planned course (your puzzle input)."""
    with open(INPUT_FILE) as file:
        lines = file.readlines()

    return list(map(parse_line, lines))


def dive(course):
    fwd = sum(c.amount for c in course if c.direction == 'forward')
    up = sum(c.amount for c in course if c.direction == 'up')
    down = sum(c.amount for c in course if c.direction == 'down')

    return (fwd, down - up)


if __name__ == '__main__':
    course = read_course_file()
    horizontal, depth = dive(course)

    print(horizontal * depth)
