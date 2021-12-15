from polymerization import *


def test_read_puzzle_input():
    polymer_template, rule_lines = read_puzzle_input()

    assert polymer_template == 'SCVHKHVSHPVCNBKBPVHV'

    assert rule_lines[0] == 'SB -> B'
    assert rule_lines[-1] == 'PH -> K'


def test_parse_insertion_rule():
    pair, insertion = parse_insertion_rule('AB -> C')

    assert pair == 'AB'
    assert insertion == 'C'


def test_count_next_step():
    start = {
        'AB': 2,
        'BC': 3,
        'AA': 0,
        'BB': 0
    }
    rules = {
        'AB': 'A',
        'BC': 'B',
        'AA': 'A',
        'BB': 'B'
    }
    next_step = count_next_step(start, rules)

    assert next_step == {
        'AB': 2,
        'BC': 3,
        'AA': 2,
        'BB': 3
    }


def test_count_chars():
    pairs = {
        'AB': 1_000,
        'AA': 1_500,
        'BA': 500
    }
    counts = count_chars(pairs, 'ABBA')

    assert counts == {
        'A': 2_501,  # Also has one extra 'A' because it's the last char from the template
        'B': 500
    }
