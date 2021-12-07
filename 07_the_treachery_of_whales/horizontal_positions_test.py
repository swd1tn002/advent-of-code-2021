from horizontal_positions import calculate_total_linear_cost_to, calculate_total_non_linear_cost_to, read_crab_coordinates
from pytest import fixture


@fixture
def advent_of_code_example():
    return [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]


def test_read_crab_coordinates():
    coordinates = read_crab_coordinates()

    assert coordinates[0] == 1101
    assert coordinates[-1] == 250


def test_calculating_linear_cost_to_correct_answer(advent_of_code_example):
    assert calculate_total_linear_cost_to(
        advent_of_code_example, 2) == 37


def test_calculating_non_linear_cost_to_correct_answer(advent_of_code_example):
    assert calculate_total_non_linear_cost_to(
        advent_of_code_example, 5) == 168
