import os
INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


def parse_line(line):
    command, amount = line.split(' ')
    return (command, int(amount))


def read_course_file():
    """The submarine seems to already have a planned course (your puzzle input)."""

    with open(INPUT_FILE) as file:
        lines = file.readlines()

    return list(map(parse_line, lines))


def dive(course):
    horizontal = 0
    depth = 0
    for command, amount in course:
        if command == 'forward':
            horizontal += amount
        elif command == 'up':
            depth -= amount
        elif command == 'down':
            depth += amount
    return (horizontal, depth)


if __name__ == '__main__':
    course = read_course_file()
    horizontal, depth = dive(course)

    print(horizontal * depth)
