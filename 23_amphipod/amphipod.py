from typing import List
from collections import namedtuple
from queue import PriorityQueue

Square = namedtuple('Square', 'row col')

puzzle = """
#############
#...........#
###C#B#A#D###
  #C#D#A#B#
  #########
"""
puzzle = [list(row) for row in puzzle.strip().split('\n')]

home_columns = {
    'A': 3,
    'B': 5,
    'C': 7,
    'D': 9
}

move_costs = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1_000
}


def is_completed(puzzle) -> bool:
    return puzzle[2][3:10] == puzzle[3][3:10] == ['A', '#', 'B', '#', 'C', '#', 'D']


def can_move_in(puzzle, start: Square, end: Square):
    # Can only move to own end columns
    char = puzzle[start[0]][start[1]]
    if end[1] != home_columns[char]:
        return False

    # If moving to upper home square, lower must already have the equal character
    if end[0] == 2 and puzzle[3][end[1]] != char:
        return False

    r0, c0 = start
    r1, c1 = end
    if c0 < c1:
        if any(x != '.' for x in puzzle[r0][c0+1:c1]):
            return False
    else:
        if any(x != '.' for x in puzzle[r0][c1:c0]):
            return False

    if r0 < r1:
        if any(row[c1] != '.' for row in puzzle[r0+1: r1+1]):
            return False
    else:
        if any(row[c1] != '.' for row in puzzle[r0+1: r1+1]):
            return False

    return True


def can_move_out(puzzle, start: Square, end: Square):
    char = puzzle[start.row][start.col]

    # TODO: move to separate function
    # Can't move out when in lower square at home base
    if start.row == 3 and home_columns[char] == start.col:
        return False

    # Can't move out when in upper square at home base and the lower is also in place
    if start.row == 2 and home_columns[char] == start.col and puzzle[start.row+1][start.col] == char:
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
    return copy, manhattan_distance * move_costs[char]


def print_puzzle(puzzle: List[List[str]]):
    for line in puzzle:
        print(''.join(line))


def move_amphipods_home(puzzle, cost):
    row = 1
    moved = True
    while moved:
        moved = False
        for i, char in enumerate(puzzle[1]):
            if char not in 'ABCD':
                continue

            current = Square(row, i)
            upper_home = Square(2, home_columns[char])
            lower_home = Square(3, home_columns[char])

            if can_move_in(puzzle, current, upper_home):
                new_puzzle, new_cost = move(puzzle, current, upper_home)
                puzzle = new_puzzle
                cost += new_cost
                moved = True

            elif can_move_in(puzzle, current, lower_home):
                new_puzzle, new_cost = move(puzzle, current, lower_home)
                puzzle = new_puzzle
                cost += new_cost
                moved = True
    return puzzle, cost


def move_amphipods_out(puzzle, cost, queue: PriorityQueue, visited: set):
    home_rows = (2, 3)
    # Squares directly above the "homes" are not allowed
    allowed_squares = set(range(1, 12)) - set(home_columns.values())
    for row in home_rows:
        for col in home_columns.values():
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
        print(f'Solved with cost {cost}')
        exit()

    if str(puzzle) not in visited:
        move_amphipods_out(puzzle, cost, queue, visited)
        visited.add(str(puzzle))


visited = set()
queue = PriorityQueue()
queue.put((0, puzzle))

while not queue.empty():
    cost, puzzle = queue.get()
    if str(puzzle) not in visited:
        solve_puzzle(puzzle, cost, queue, visited)
