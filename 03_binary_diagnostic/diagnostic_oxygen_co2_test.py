from diagnostic import convert_to_bits
from diagnostic_oxygen_co2 import find_oxygen_generator_rating, find_co2_generator_rating
from pytest import fixture


@fixture
def sample_report():
    input_file = '00100,11110,10110,10111,10101,01111,00111,11100,10000,11001,00010,01010'
    return list(map(convert_to_bits, input_file.split(',')))


def test_find_oxygen_generator_rating(sample_report):
    oxygen_rating = find_oxygen_generator_rating(sample_report)
    assert oxygen_rating == 23


def test_find_co2_generator_rating(sample_report):
    co2_rating = find_co2_generator_rating(sample_report)
    assert co2_rating == 10
