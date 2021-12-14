from typing import Tuple, Dict, List
import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


def read_puzzle_input(filename=INPUT_FILE) -> List[str]:
    """
    The submarine manual contains instructions for finding the optimal polymer formula;
    specifically, it offers a polymer template and a list of pair insertion rules (your puzzle input).

    Returns a tuple with the polymer template and the list of rules
    """
    with open(filename) as file:
        lines = file.read().split('\n')

    return lines[0], lines[2:]


def generate_insertion_rules(rule_lines: List[str]) -> Dict[str, str]:
    return dict((parse_insertion_rule(line)) for line in rule_lines)


def parse_insertion_rule(line: str) -> Tuple[str, str]:
    """
    A rule like AB -> C means that when elements A and B are immediately adjacent,
    element C should be inserted between them. These insertions all happen simultaneously.

    This method parses a signle rule and returns the pair and the insertion char.
    """
    pair, insertion = line.split(' -> ')
    return pair, insertion


def count_next_step_pairs(pairs_and_counts: Dict[str, int], insertion_rules: Dict[str, str]) -> Dict[str, int]:
    """
    Note that these pairs overlap: the second element of one pair is the first element of the next pair.
    Also, because all pairs are considered simultaneously, inserted elements are not considered to be part
    of a pair until the next step.
    """
    new_counts = {pair: 0 for pair in insertion_rules.keys()}

    for pair, count in pairs_and_counts.items():
        insert_char = insertion_rules[pair]
        new_counts[pair[0] + insert_char] += count
        new_counts[insert_char + pair[1]] += count

    return new_counts


def count_first_chars(pair_counts: Dict[str, int], polymer_template: str) -> Dict[str, int]:
    char_counts = {c: 0 for pair in pair_counts.keys() for c in pair}

    # To count each character only once, we only take the first character of each pair
    for pair, count in pair_counts.items():
        char_counts[pair[0]] += count

    # The last character in the polymer does not appear as the first of any pair,
    # so it needs to be incremented manually
    char_counts[polymer_template[-1]] += 1

    return char_counts


if __name__ == '__main__':
    polymer_template, rule_lines = read_puzzle_input()
    insertion_rules = generate_insertion_rules(rule_lines)

    # Initialize a pair count dict with counts from the initial polymer template
    pair_counts = {
        pair: polymer_template.count(pair) for pair in insertion_rules.keys()
    }

    # Part 1
    for i in range(10):
        pair_counts = count_next_step_pairs(pair_counts, insertion_rules)

    # What do you get if you take the quantity of the most common element and subtract
    # the quantity of the least common element?
    counts_1 = count_first_chars(pair_counts, polymer_template)

    # 2712
    print(f'Part 1: {max(counts_1.values()) - min(counts_1.values())}')

    # Part 2, do 30 more steps
    for i in range(30):
        pair_counts = count_next_step_pairs(pair_counts, insertion_rules)

    counts_2 = count_first_chars(pair_counts, polymer_template)

    # 8336623059567
    print(f'Part 2: {max(counts_2.values()) - min(counts_2.values())}')
