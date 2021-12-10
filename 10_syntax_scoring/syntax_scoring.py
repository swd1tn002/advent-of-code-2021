import re
import os
from typing import List

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


def read_input(filename: str = INPUT_FILE) -> List[str]:
    """
    You bring up a copy of the navigation subsystem (your puzzle input).

    The navigation subsystem syntax is made of several lines containing
    chunks. There are one or more chunks on each line, and chunks contain 
    zero or more other chunks.
    """
    with open(filename) as file:
        return file.read().split('\n')


def get_corrupted(lines: List[str]) -> List[str]:
    """
    Returns a new list with only corrupted lines from the input.
    """
    return [line for line in lines if is_corrupted(line)]


def get_incomplete(lines: List[str]) -> List[str]:
    return [line for line in lines if not is_corrupted(line)]


def is_corrupted(line: str) -> bool:
    """
    A corrupted line is one where a chunk closes with the wrong character - that
    is, where the characters it opens and closes with do not form one of the four 
    legal pairs listed above.
    """
    return get_first_illegal(line) != None


def get_first_illegal(line: str) -> str:
    """
    Returns the first illegal parenthesis end character found on the given line, 
    or None if it has no illegal end characters.
    """
    illegal = [')', ']', '>', '}']
    return next(iter(c for c in remove_legal_chunks(line) if c in illegal), None)


def remove_legal_chunks(line: str) -> str:
    """
    Repeatedly removes all legal chunks <>, {}, [], and () until 
    no valid chunks remain.
    """
    valid = r'(<>)|({})|(\[\])|(\(\))'

    previous = None
    while previous != line:
        previous = line
        line = re.sub(valid, '', line)

    return line


def get_syntax_error_score(line: str) -> int:
    """
    To calculate the syntax error score for a line, take the first illegal
    character on the line and look it up in the following table.
    """
    scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
    return scores.get(get_first_illegal(line), 0)


def close_incomplete_line(incomplete: str) -> str:
    """
    You can only use closing characters (), ], }, or >), and you must add
    them in the correct order so that only legal pairs are formed and all 
    chunks end up closed.
    """
    open_chunks = remove_legal_chunks(incomplete)
    reverse = ''.join(reversed(open_chunks))
    return reverse.replace('{', '}') .replace('[', ']').replace('<', '>').replace('(', ')')


def get_syntax_completion_score(chars: str) -> int:
    """
    The score is determined by considering the completion string character-by-character.
    Start with a total score of 0. Then, for each character, multiply the total score 
    by 5 and then increase the total score by the point value given for the character
    in the following table:
    """
    scores = {')': 1, ']': 2, '}': 3, '>': 4}
    total = 0
    for c in chars:
        total *= 5
        total += scores[c]
    return total


if __name__ == '__main__':
    input = read_input()

    # Part 1
    # What is the total syntax error score for those errors?
    syntax_err_score = sum(get_syntax_error_score(line)
                           for line in get_corrupted(input))

    print(syntax_err_score)

    # Part 2
    # The winner is found by sorting all of the scores and then taking the middle score.
    scores = sorted([get_syntax_completion_score(close_incomplete_line(
        incomplete)) for incomplete in get_incomplete(input)])

    print(scores[len(scores) // 2])
