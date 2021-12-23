from typing import List
from collections import namedtuple
from queue import PriorityQueue

Square = namedtuple('Square', 'row col')

HOME_COLUMNS = {
    'A': 3,
    'B': 5,
    'C': 7,
    'D': 9
}

MOVE_COSTS = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1_000
}


def is_completed(puzzle) -> bool:
    home_rows = puzzle[2:-1]
    return all(row[3:10] == ['A', '#', 'B', '#', 'C', '#', 'D'] for row in home_rows)


def can_move_in(puzzle, start: Square, end: Square):
    # Can only move to own end columns or "rooms"
    char = puzzle[start.row][start.col]

    if end.col != HOME_COLUMNS[char]:
        return False

    # If moving to a square inside "home room", all previous squares must
    # already have the equal character
    if any(puzzle[r][end.col] != char for r in range(end.row+1, len(puzzle)-1)):
        return False

    # Moving to the right or to the left:
    if any(x != '.' for x in puzzle[start.row][start.col+1:end.col+1] + puzzle[start.row][end.col:start.col]):
        return False

    # Moving in the home cells (row increases)
    if any(row[end.col] != '.' for row in puzzle[start.row+1: end.row+1]):
        return False

    return True


def can_move_out(puzzle, start: Square, end: Square):
    char = puzzle[start.row][start.col]

    # Moving out of the home room is not allowed if all previous chars are in correct places
    if HOME_COLUMNS[char] == start.col and all(puzzle[r][start.col] == char for r in range(start.row, len(puzzle) - 1)):
        return False

    if any(row[start.col] != '.' for row in puzzle[end.row: start.row]):
        return False

    if any(x != '.' for x in puzzle[end.row][end.col:start.col] + puzzle[end.row][start.col+1:end.col+1]):
        return False

    return True


def move(puzzle, start: Square, end: Square):
    char = puzzle[start.row][start.col]
    copy = [row[:] for row in puzzle]

    copy[end.row][end.col] = char
    copy[start.row][start.col] = '.'

    manhattan_distance = abs(start.row - end.row) + abs(start.col - end.col)
    return copy, manhattan_distance * MOVE_COSTS[char]


def print_puzzle(puzzle: List[List[str]]):
    for line in puzzle:
        print(''.join(line))


def move_amphipods_home(puzzle, cost):
    """
    Moving amphipods to home can open up the way to previously 
    blocked ones, so this needs to be repeated with recursion.
    """
    row = 1

    for i, char in enumerate(puzzle[1]):
        if char not in 'ABCD':
            continue

        current = Square(row, i)
        home_squares = [Square(r, HOME_COLUMNS[char])
                        for r in range(2, len(puzzle)-1)]

        for home in home_squares:
            if can_move_in(puzzle, current, home):
                new_puzzle, new_cost = move(puzzle, current, home)
                return move_amphipods_home(new_puzzle, cost + new_cost)

    return puzzle, cost


def move_amphipods_out(puzzle, cost, queue: PriorityQueue, visited: set):
    # Squares directly above the "homes" are not allowed
    allowed_squares = set(range(1, 12)) - set(HOME_COLUMNS.values())
    for row in range(2, len(puzzle) - 1):
        for col in HOME_COLUMNS.values():
            current = Square(row, col)
            if puzzle[row][col] in 'ABCD':
                for x in allowed_squares:
                    if can_move_out(puzzle, current, Square(1, x)):
                        #print(f'{puzzle[row][col]} can move to {x}')
                        new_puzzle, new_cost = move(
                            puzzle, current, Square(1, x))

                        new_puzzle, new_cost = move_amphipods_home(
                            new_puzzle, new_cost)
                        if str(new_puzzle) not in visited:
                            queue.put((cost + new_cost, new_puzzle))


def solve_puzzle(puzzle, cost, queue, visited):
    if is_completed(puzzle):
        return puzzle, cost

    if str(puzzle) not in visited:
        move_amphipods_out(puzzle, cost, queue, visited)
        visited.add(str(puzzle))
    return None, None


if __name__ == '__main__':
    puzzle = """
#############
#...........#
###C#B#A#D###
  #C#D#A#B#
  #########
"""
    puzzle = [list(row) for row in puzzle.strip().split('\n')]

    visited = set()
    queue = PriorityQueue()
    queue.put((0, puzzle))
    solution = None

    while not solution and not queue.empty():
        cost, puzzle = queue.get()
        if str(puzzle) not in visited:
            solution, cost = solve_puzzle(puzzle, cost, queue, visited)
            if solution:
                print(f'Solved with cost {cost}!')
                print_puzzle(puzzle)
