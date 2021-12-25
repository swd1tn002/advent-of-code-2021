import os


INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


def read_input_file(file=INPUT_FILE) -> str:
    """
    There are two herds of sea cucumbers sharing the same region; one always moves east (>),
    while the other always moves south (v). Each location can contain at most one sea cucumber;
    the remaining locations are empty (.). The submarine helpfully generates a map of the 
    situation (your puzzle input)
    """
    with open(file) as f:
        return f.read()


def move_sea_cucumbers(floor: str) -> str:
    """
    There are two herds of sea cucumbers sharing the same region; one always moves east (>), 
    while the other always moves south (v).

    When a herd moves forward, every sea cucumber in the herd first simultaneously considers 
    whether there is a sea cucumber in the adjacent location it's facing (even another sea
    cucumber facing the same direction), and then every sea cucumber facing an empty location
    simultaneously moves into that location.

    Every step, the sea cucumbers in the east-facing herd attempt to move forward one
    location, then the sea cucumbers in the south-facing herd attempt to move forward one location.
    """
    return _move_south(_move_east(floor))


def _move_east(floor: str) -> str:
    lines = [
        # sea cucumbers that move off the right edge of the map appear on the left edge
        (line[-1] + line + line[0]).replace('>.', '.>')[1:-1]
        for line in floor.split('\n')
    ]
    return '\n'.join(lines)


def _move_south(floor: str) -> str:
    """
    "Horizontal lines" are easier to manipulate than vertical, so the ocean floor is
    transposed before and after the needed operations.
    """
    floor = _transpose_floor(floor)
    lines = [
        # sea cucumbers that move off the bottom edge of the map appear on the top edge
        (line[-1] + line + line[0]).replace('v.', '.v')[1:-1]
        for line in floor.split('\n')
    ]
    return _transpose_floor('\n'.join(lines))


def count_steps_until_stable(floor: str, max=1_000) -> int:
    """
    This function returns the first step on which no sea cucumbers move.
    """
    previous = floor
    for i in range(1, max+1):
        floor = move_sea_cucumbers(floor)
        if floor == previous:
            return i
        else:
            previous = floor

    return -1


def _transpose_floor(floor: str) -> str:
    """
    Returns a copy of the given ocean floor where the x and y axes have been swapped.

    ab      ac
    cd  =>  bd
    """
    lines = floor.split('\n')
    height = len(lines)
    width = len(lines[0])

    rotated = [[' '] * height for _ in range(width)]

    for y in range(height):
        for x in range(width):
            rotated[x][y] = lines[y][x]

    return '\n'.join(''.join(chars) for chars in rotated)


if __name__ == '__main__':
    floor = read_input_file()

    # Part 1: What is the first step on which no sea cucumbers move?
    steps = count_steps_until_stable(floor)
    print(f'Part 1: sea cucumbers stop moving after {steps} steps')
