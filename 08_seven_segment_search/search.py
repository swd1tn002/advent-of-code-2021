import os
from typing import List, Set
from collections import namedtuple

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

Note = namedtuple('Note', 'patterns output')


def read_notes(filename=INPUT_FILE) -> List[Note]:
    """
    Each entry consists of ten unique signal patterns, a | delimiter,
    and finally the four digit output value. Within an entry, the same
    wire/segment connections are used (but you don't know what the
    connections actually are).
    """
    with open(filename) as file:
        return list(map(parse_note, file.readlines()))


def parse_note(entry: str) -> Note:
    """
    Converts single line in input, for example:
    "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
    into a Note with a set of segment patterns and a list of encoded outputs.
    """
    patterns, output = entry.split('|')
    patterns = set(map(sort_str, patterns.split()))
    output = list(map(sort_str, output.split()))

    return Note(patterns, output)


def sort_str(input: str) -> str:
    """
    The signals which control the segments have been mixed up on each display. This function
    sorts the segments alphabetically for consistent comparisons.
    """
    return ''.join(sorted(input))


def decode_notes(notes: List[Note]) -> List[List[int]]:
    """
    Transforms a list of Note objects into a list of int vectors based on the
    patterns and encoded outputs in each individual Note.
    """
    return list(map(decode_note, notes))


def decode_note(note: Note) -> List[str]:
    """
    Decodes a Note with a set of patterns and a list of encoded digits int a list of ints
    "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf" => [5, 3, 5, 3]
    """
    decoders = [decode_zero, decode_one, decode_two,
                decode_three, decode_four, decode_five,
                decode_six, decode_seven, decode_eight, decode_nine]

    # creates a dict with the segment patterns as keys and their corresponding ints as values
    decoded = {func(note.patterns): i for (i, func) in enumerate(decoders)}

    return [decoded[x] for x in note.output]


def decode_zero(patterns: Set[int]) -> str:
    # Only remaining with length 6 is zero
    six_segments = filter_by_length(patterns, 6)
    six = decode_six(patterns)
    nine = decode_nine(patterns)

    return next(iter(set(six_segments) - {six, nine}))


def decode_one(patterns: Set[str]) -> str:
    # 1 is the only digit that uses two segments
    return filter_by_length(patterns, 2)[0]


def decode_two(patterns: Set[str]) -> str:
    # When we know three and five, we can eliminate them to discover two
    five_segments = filter_by_length(patterns, 5)
    three = decode_three(patterns)
    five = decode_five(patterns)

    return next(iter(set(five_segments) - {three, five}))


def decode_three(patterns: Set[str]) -> str:
    # Three is the only 5 segment number, which contains both segments from 1
    five_segments = filter_by_length(patterns, 5)
    one = set(decode_one(patterns))
    return next(x for x in five_segments if len(set(x) & set(one)) == 2)


def decode_four(patterns: Set[str]) -> str:
    # 4 is the only digit that has four segments
    return filter_by_length(patterns, 4)[0]


def decode_six(patterns: Set[str]) -> str:
    # Number 6 has six segments, but unlike others, 6 only contains one segment from 1.
    six_segments = filter_by_length(patterns, 6)
    one = decode_one(patterns)
    return next(code for code in six_segments if len(set(one) - set(code)) == 1)


def decode_five(patterns: Set[str]) -> str:
    # Five is the only five segment number that has the top left segment on.
    # The top left segment can be calculated by reducing segments 4 - 3.
    five_segments = filter_by_length(patterns, 5)
    four = set(decode_four(patterns))
    three = set(decode_three(patterns))
    top_left_segment = four - three

    return next(x for x in five_segments if top_left_segment & set(x))


def decode_seven(patterns: Set[str]) -> str:
    # 7 is the only digit that uses three segments
    return filter_by_length(patterns, 3)[0]


def decode_eight(patterns: Set[str]) -> str:
    # 8 is the only digit that uses all 7 segments
    return filter_by_length(patterns, 7)[0]


def decode_nine(patterns: Set[str]) -> str:
    # Nine is the number that has 6 segments, one of which the number 3 does not have.
    six_segments = filter_by_length(patterns, 6)
    three = decode_three(patterns)
    return next(x for x in six_segments if len(set(x) - set(three)) == 1)


def filter_by_length(patterns: Set[str], length: int) -> List[str]:
    """
    Returns as a list the patterns which have the given length.
    """
    return [p for p in patterns if len(p) == length]


def list_to_int(nums):
    return int(''.join(map(str, nums)))


if __name__ == '__main__':
    notes = read_notes()
    decoded = decode_notes(notes)

    for numbers in decoded:
        print(numbers)

    as_ints = [list_to_int(nums) for nums in decoded]
    as_str = ''.join(map(str, as_ints))

    count_1_4_7_8 = as_str.count(
        '1') + as_str.count('4') + as_str.count('7') + as_str.count('8')
    total = sum(as_ints)

    print(f'Part 1: count is {count_1_4_7_8}.')
    print(f'Part 2: Sum is {total}.')
