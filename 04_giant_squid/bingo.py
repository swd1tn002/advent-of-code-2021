from typing import List
import os
INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


def str_to_list_of_ints(line: str) -> List[int]:
    """
    Converts " 1,  2,  3" to [1, 2, 3]
    """
    return list(map(int, line.split()))


def board_chunk_to_int_matrix(chunk: str) -> List[List[int]]:
    """
    Converts string "1, 2\n3, 4" to matrix [[1, 2], [3, 4]]
    """
    return list(map(str_to_list_of_ints, chunk.splitlines()))


def read_bingo_input() -> tuple:
    """
    Reads the random order in which to draw numbers and the random set of boards.
    Returns tuple (numbers: List[int], boards: List[List[List[int]]])
    """
    with open(INPUT_FILE) as file:
        chunks = file.read().split('\n\n')

    drawn_numbers = list(map(int, chunks[0].split(',')))
    boards = map(board_chunk_to_int_matrix, chunks[1:])

    return drawn_numbers, list(boards)


def check_winner(bingo_board: List[List[int]], marked: List[int]) -> bool:
    """
    If all numbers in any row or any column of a board are marked, that board wins. 
    Diagonals don't count.
    """
    transpose = list(zip(*bingo_board))  # gets the vertical lines
    all_lines = bingo_board + transpose
    return any(len(set(row) - set(marked)) == 0 for row in all_lines)


def find_winner(boards: List[List[List[int]]], drawn_numbers: List[int]) -> List[List[int]]:
    """
    Figure out which board will win first.
    """
    for round in range(len(boards[0][0]), len(drawn_numbers) + 1):
        numbers = drawn_numbers[:round]

        winners = [board for board in boards if check_winner(board, numbers)]
        if winners:
            return winners[0], numbers

    return None, drawn_numbers


def find_loser(boards: List[List[List[int]]], drawn_numbers: List[int]) -> List[List[int]]:
    """
    Figure out which board will win last and choose that one.
    """
    remaining = boards

    for round in range(len(boards[0][0]), len(drawn_numbers) + 1):
        numbers = drawn_numbers[:round]

        losers = [board for board in remaining if check_winner(
            board, numbers) == False]

        if len(losers) == 0:
            return remaining[0], numbers

        remaining = losers

    return None, drawn_numbers


def calculate_score(board: List[List[int]], marked: List[int]) -> int:
    """
    Start by finding the sum of all unmarked numbers on that board.
    Then, multiply that sum by the number that was just called when the board won,
    to get the final score.
    """
    all_numbers = {num for row in board for num in row}
    not_marked = all_numbers - set(marked)

    multiplier = marked[-1]
    return sum(not_marked) * multiplier


if __name__ == '__main__':
    numbers_drawn, boards = read_bingo_input()

    winner, winning_marked = find_winner(boards, numbers_drawn)
    winning_score = calculate_score(winner, winning_marked)

    print(f'Winning score: {winning_score}')

    loser, losing_marked = find_loser(boards, numbers_drawn)
    losing_score = calculate_score(loser, losing_marked)

    print(f'Losing score: {losing_score}')
