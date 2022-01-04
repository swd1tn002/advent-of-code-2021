from typing import List
import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


def read_crab_coordinates(filename=INPUT_FILE) -> List[int]:
    """
    You quickly make a list of the horizontal position of each crab (your puzzle input)
    """
    with open(filename) as file:
        return list(map(int, file.read().split(',')))


def get_distances_to(numbers: List[int], target: int) -> List[int]:
    return [abs(current - target) for current in numbers]


def calculate_total_linear_cost_to(items: List[int], target: int) -> int:
    """
    How much fuel must the crabs (items) spend to the target position?
    """
    return sum(get_distances_to(items, target))


def calculate_total_non_linear_cost_to(positions: List[int], target: int) -> int:
    """
    As it turns out, crab submarine engines don't burn fuel at a constant rate.
    """
    distances = get_distances_to(positions, target)
    return sum(_get_non_linear_cost(distance) for distance in distances)


def _get_non_linear_cost(distance: int) -> int:
    """
    Each change of 1 step in horizontal position costs 1 more unit of
    fuel than the last: the first step costs 1, the second step costs 2, the
    third step costs 3, and so on.
    """
    return distance * (distance + 1) // 2


if __name__ == '__main__':
    crabs = read_crab_coordinates()

    costs_per_guess_1 = [calculate_total_linear_cost_to(
        crabs, guess) for guess in range(0, max(crabs))]

    # Part 1: Crab submarines have limited fuel, so you need to find a way to make all of their
    # horizontal positions match while requiring them to spend as little fuel as possible.
    min_fuel_1 = min(costs_per_guess_1)
    best_guess_1 = costs_per_guess_1.index(min_fuel_1)

    print(f'First part: Moce crabs to {best_guess_1} with cost: {min_fuel_1}')

    # Part 2: As it turns out, crab submarine engines don't burn fuel at a constant rate.
    costs_per_guess_2 = [calculate_total_non_linear_cost_to(
        crabs, guess) for guess in range(0, max(crabs))]

    min_fuel_2 = min(costs_per_guess_2)
    best_guess_2 = costs_per_guess_2.index(min_fuel_2)
    print(f'Second part: Moce crabs to {best_guess_2} with cost: {min_fuel_2}')
