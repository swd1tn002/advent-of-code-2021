import os
from typing import List
from collections import namedtuple

input = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"

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
    patterns, output = entry.split('|')
    patterns = list(map(sort_str, patterns.split()))
    output = list(map(sort_str, output.split()))

    return Note(patterns, output)


def sort_str(input: str) -> str:
    return ''.join(sorted(input))


def decode_notes(notes: List[Note]) -> List[List[int]]:
    return list(map(decode_note, notes))


def decode_note(note: Note) -> List:
    decoded = dict([(decode_zero(note.patterns), 0),
                    (decode_one(note.patterns), 1),
                    (decode_two(note.patterns), 2),
                    (decode_three(note.patterns), 3),
                    (decode_four(note.patterns), 4),
                    (decode_five(note.patterns), 5),
                    (decode_six(note.patterns), 6),
                    (decode_seven(note.patterns), 7),
                    (decode_eight(note.patterns), 8),
                    (decode_nine(note.patterns), 9)])

    return [decoded[x] for x in note.output if x in decoded]


def decode_zero(patterns: List[int]) -> str:
    # Only remaining with length 6 is zero
    len_six = filter_by_length(patterns, 6)
    six = decode_six(patterns)
    nine = decode_nine(patterns)
    return [*(set(len_six) - {six, nine})][0]


def decode_one(patterns: List[str]) -> str:
    return filter_by_length(patterns, 2)[0]


def decode_two(patterns: List[str]) -> str:
    len_five = filter_by_length(patterns, 5)
    three = decode_three(patterns)
    five = decode_five(patterns)
    return [x for x in len_five if x != three and x != five][0]


def decode_three(patterns: List[str]) -> str:
    # Length is 5, contains both segments from 1
    one = set(decode_one(patterns))
    len_five = filter_by_length(patterns, 5)
    return [x for x in len_five if len(set(x) & set(one)) == 2][0]


def decode_four(patterns: List[str]) -> str:
    # 4 is the only digit that uses four segments
    return filter_by_length(patterns, 4)[0]


def decode_six(patterns: List[str]) -> str:
    # Number 6: length 6, but not 9. Does not contain all segments from 1.
    len_six = filter_by_length(patterns, 6)
    one = decode_one(patterns)
    return [x for x in len_six if len(set(one) - set(x)) == 1][0]


def decode_five(patterns: List[str]) -> str:
    # Length is 5, but is not three. Contains a segment, that neither 7 nor 3 contain, unlike number 2
    len_five = filter_by_length(patterns, 5)
    four = set(decode_four(patterns))
    three = set(decode_three(patterns))
    top_left = four - three
    return [x for x in len_five if len(top_left - set(x)) == 0][0]


def decode_seven(patterns: List[str]) -> str:
    # 7 is the only digit that uses three segments
    return filter_by_length(patterns, 3)[0]


def decode_eight(patterns: List[str]) -> str:
    # 8 is the only digit that uses all 7 segments
    return filter_by_length(patterns, 7)[0]


def decode_nine(patterns: List[str]) -> str:
    three = decode_three(patterns)
    len_six = filter_by_length(patterns, 6)
    return [x for x in len_six if len(set(x) - set(three)) == 1][0]


def filter_by_length(patterns: List[str], length: int) -> List[str]:
    return [p for p in patterns if len(p) == length] or ['?']


if __name__ == '__main__':
    notes = read_notes()
    total = 0
    for note in notes:
        decoded = decode_note(note)
        print(decoded)

        as_number = ''.join(map(str, decoded))
        total += int(as_number)

    print(f'Sum: {total}')
