from dive import read_course_file


def dive_with_aim(course):
    aim = 0
    horizontal = 0
    depth = 0

    for command, amount in course:
        if command == 'forward':
            horizontal += amount
            depth += aim * amount
        elif command == 'up':
            aim -= amount
        elif command == 'down':
            aim += amount
    return (horizontal, depth)


if __name__ == '__main__':
    course = read_course_file()
    horizontal, depth = dive_with_aim(course)

    print(horizontal * depth)
