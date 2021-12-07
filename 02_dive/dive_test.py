from dive import read_course_file, parse_line, dive, Command


def test_reading_submarine_course():
    instructions = read_course_file()

    assert instructions[0] == ('forward', 8)
    assert instructions[-1] == ('forward', 4)


def test_parsing_line():
    command, amount = parse_line('forward 8')

    assert command == 'forward'
    assert amount == 8


def test_dive():
    horizontal, depth = dive([
        Command('forward', 5),
        Command('down', 5),
        Command('forward', 8),
        Command('up', 3),
        Command('down', 8),
        Command('forward', 2)
    ])
    assert horizontal == 15
    assert depth == 10
