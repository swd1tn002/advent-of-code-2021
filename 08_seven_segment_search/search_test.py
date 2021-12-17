from search import *
from pytest import fixture


@fixture
def sample_input():
    return 'acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'


def test_parse_note(sample_input):
    note = parse_note(sample_input)

    assert note.patterns == {'abcdefg', 'bcdef', 'acdfg',
                             'abcdf', 'abd', 'abcdef', 'bcdefg', 'abef', 'abcdeg', 'ab'}
    assert note.output == ['bcdef', 'abcdf', 'bcdef', 'abcdf']


def test_decode_one(sample_input):
    note = parse_note(sample_input)
    assert decode_one(note.patterns) == 'ab'


def test_decode_four(sample_input):
    note = parse_note(sample_input)
    assert decode_four(note.patterns) == 'abef'


def test_decode_seven(sample_input):
    note = parse_note(sample_input)
    assert decode_seven(note.patterns) == 'abd'
