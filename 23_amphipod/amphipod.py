from typing import List, Tuple
from collections import namedtuple
from queue import PriorityQueue
import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


Square = namedtuple('Square', 'row col')
Puzzle = List[List[str]]

"""
The amphipods would like a method to organize every amphipod into side rooms
so that each side room contains one type of amphipod and the types are sorted
A-D going left to right, like this:
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
"""
HOME_COLUMNS = {
    'A': 3,
    'B': 5,
    'C': 7,
    'D': 9
}

"""
Amber amphipods require 1 energy per step, Bronze amphipods require 10 energy, 
Copper amphipods require 100, and Desert ones require 1000.
"""
MOVE_COSTS = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1_000
}


def is_completed(puzzle: Puzzle) -> bool:
    """
    Returns True if all amphipods in the puzzle are in their own rooms.
    """
    home_rows = puzzle[2:-1]
    return all(row[3:10] == ['A', '#', 'B', '#', 'C', '#', 'D'] for row in home_rows)


def can_move_in(puzzle: Puzzle, start: Square, end: Square) -> bool:
    """
    This function determines if the amphipod in the given start square in the hallway can
    move to the given end square in a room.

    Amphipods will never move from the hallway into a room unless that room is their 
    destination room and that room contains no amphipods which do not also have that room 
    as their own destination.
    """
    char = puzzle[start.row][start.col]
    hallway = puzzle[start.row]

    # Can only move to own end columns or "rooms"
    if end.col != HOME_COLUMNS[char]:
        return False

    # Room contains no amphipods which do not also have that room as their own destination.
    # They also fill the room from the end, so no empty squares are allowed.
    if any(puzzle[r][end.col] != char for r in range(end.row+1, len(puzzle)-1)):
        return False

    # Can the amphipod move horizontally in the hallway to the room?
    if any(x != '.' for x in hallway[start.col+1:end.col+1] + hallway[end.col:start.col]):
        return False

    # Are all vertical squares empty so the route is clear?
    if any(row[end.col] != '.' for row in puzzle[start.row+1: end.row+1]):
        return False

    # No obstacles found
    return True


def can_move_out(puzzle, start: Square, end: Square):
    """
    Amphipods can move up, down, left, or right so long as they are moving into an unoccupied
    open space. Once an amphipod stops moving in the hallway, it will stay in that spot until
    it can move into a room.
    """
    char = puzzle[start.row][start.col]
    in_home_room = (HOME_COLUMNS[char] == start.col)

    # Moving out of the home room is not allowed if all previous chars are in correct places
    if in_home_room and all(puzzle[r][start.col] == char for r in range(start.row, len(puzzle) - 1)):
        return False

    # Is the passage to hallway is blocked?
    if any(row[start.col] != '.' for row in puzzle[end.row: start.row]):
        return False

    # Is the hallway clear for horizontal movement?
    hallway = puzzle[end.row]
    if any(x != '.' for x in hallway[end.col:start.col] + hallway[start.col+1:end.col+1]):
        return False

    return True


def move(puzzle: Puzzle, start: Square, end: Square) -> Tuple[Puzzle, int]:
    """
    Amphipods can move up, down, left, or right so long as they are moving into an unoccupied
    open space. Each type of amphipod requires a different amount of energy to move one step.

    This function creates a copy of the given puzzle with the given movement applied, and
    the energy consumed with the movement.

    This function does not check if the route is clear for movement, check that first.
    """

    copy = [row[:] for row in puzzle]
    char = puzzle[start.row][start.col]

    copy[end.row][end.col] = char
    copy[start.row][start.col] = '.'

    manhattan_distance = abs(start.row - end.row) + abs(start.col - end.col)
    return copy, manhattan_distance * MOVE_COSTS[char]


def print_puzzle(puzzle: Puzzle):
    """
    Prints the given Puzzle as in the puzzle instructions.
    """
    for line in puzzle:
        print(''.join(line))


def move_amphipods_home(puzzle: Puzzle, cost: int) -> Tuple[Puzzle, int]:
    """
    Moves all amphipods in their home rooms that can be moved.
    Moving amphipods to home can open up the way to previously
    blocked ones, so this needs to be repeated with recursion.

    Returns a new Puzzle with the end cost after the operations.
    """
    hallway = 1

    for i, char in enumerate(puzzle[1]):
        if char not in 'ABCD':
            continue

        current = Square(hallway, i)
        home_squares = [Square(r, HOME_COLUMNS[char])
                        for r in range(2, len(puzzle)-1)]

        for home in home_squares:
            if can_move_in(puzzle, current, home):
                new_puzzle, new_cost = move(puzzle, current, home)
                return move_amphipods_home(new_puzzle, cost + new_cost)

    return puzzle, cost


def move_amphipods_out(puzzle, cost, queue: PriorityQueue, visited: set):
    """
    Amphipods will never stop on the space immediately outside any room (HOME_COLUMNS).
    They can move into that space so long as they immediately continue moving.

    This function creates new puzzle states and adds them with their cumulative costs
    into the priority queue for later traversing.
    """
    hallway_squares = set(range(1, 12)) - set(HOME_COLUMNS.values())

    # Iterate over all amphipods in rooms and move them to the hallway one-by-one
    for row in range(2, len(puzzle) - 1):
        for col in HOME_COLUMNS.values():
            current = Square(row, col)
            if puzzle[row][col] in 'ABCD':
                for destination in hallway_squares:
                    if can_move_out(puzzle, current, Square(1, destination)):
                        out_step, out_cost = move(
                            puzzle, current, Square(1, destination))
                        in_step, in_cost = move_amphipods_home(
                            out_step, out_cost)
                        if str(in_step) not in visited:
                            queue.put((cost + in_cost, in_step))


def solve_puzzle(puzzle: Puzzle) -> Tuple[Puzzle, int]:
    """
    Use a priority queue to find the shortest path to a completed puzzle by moving
    amphipohds out to the hallway and back in the rooms one step at a time.

    Returns the completed puzzle and the cost to that solution or (None, None).
    """
    visited = set()
    queue = PriorityQueue()
    queue.put((0, puzzle))
    solution = None

    while not solution and not queue.empty():
        cost, puzzle = queue.get()

        if is_completed(puzzle):
            return puzzle, cost

        if str(puzzle) not in visited:
            move_amphipods_out(puzzle, cost, queue, visited)
            visited.add(str(puzzle))

    return None, None


def read_puzzle_input(file: str = INPUT_FILE) -> Puzzle:
    """
    "They give you a diagram of the situation, including locations of each amphipod
    (A, B, C, or D, each of which is occupying an otherwise open space), walls (#),
    and open space (.)."
    """
    with open(file) as f:
        puzzle = f.read()

    return [list(row) for row in puzzle.strip().split('\n')]


if __name__ == '__main__':
    """
    Part 1: What is the least energy required to organize the amphipods?
    """
    puzzle = read_puzzle_input()

    solution1, part1_cost = solve_puzzle(puzzle)
    print(f'Part 1 solved with cost {part1_cost}')

    """
    Part 2:
    As you prepare to give the amphipods your solution, you notice that the diagram 
    they handed you was actually folded up. As you unfold it, you discover an extra
    part of the diagram.

    Using the initial configuration from the full diagram, what is the least energy
    required to organize the amphipods?
    """
    puzzle2 = puzzle[:3] + \
        [list('  #D#C#B#A#'), list('  #D#B#A#C#')] + puzzle[-2:]

    solution2, part2_cost = solve_puzzle(puzzle2)
    print(f'Part 2 solved with cost {part2_cost}')
