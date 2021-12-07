from typing import List
import os
INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


def read_crab_coordinates(filename=INPUT_FILE) -> List[int]:
    with open(filename) as file:
        return list(map(int, file.read().split(',')))


def get_distances_to(numbers: List[int], target: int) -> List[int]:
    return [abs(current - target) for current in numbers]


def calculate_total_linear_cost_to(items: List[int], target: int) -> int:
    return sum(get_distances_to(items, target))


def calculate_total_non_linear_cost_to(positions: List[int], target: int) -> int:
    known_costs = {}
    distances = get_distances_to(positions, target)
    return sum(_get_non_linear_cost(distance, known_costs) for distance in distances)


def _get_non_linear_cost(distance: int, cache: dict) -> int:
    if distance in cache:
        return cache[distance]
    else:
        cost = sum(i for i in range(0, distance+1))
        cache[distance] = cost
        return cost


if __name__ == '__main__':
    crabs = read_crab_coordinates()

    costs_1 = [calculate_total_linear_cost_to(
        crabs, i) for i in range(0, max(crabs))]

    # Part 1
    min_cost_1 = min(costs_1)
    position_1 = costs_1.index(min_cost_1)

    print(f'First part: Moce crabs to {position_1} with cost: {min_cost_1}')

    # Part 2
    costs_2 = [calculate_total_non_linear_cost_to(
        crabs, i) for i in range(0, max(crabs))]
    min_cost_2 = min(costs_2)
    position_2 = costs_2.index(min_cost_2)
    print(f'Second part: Moce crabs to {position_2} with cost: {min_cost_2}')
