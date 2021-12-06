from typing import List
import os
INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


def read_population_ages(filename=INPUT_FILE) -> List[int]:
    """
    The submarine automatically produces a list of the ages of several
    hundred nearby lanternfish (your puzzle input).

    Returns the population in a list grouped to list indices by their ages,
    for example '1,1,3,3,0,3' => [1, 2, 3, 0, 0, 0, 0, 0]
    """
    with open(filename) as file:
        ages = list(map(int, file.read().split(',')))
        grouped = [0] * 9
        for age in ages:
            grouped[age] += 1
    return grouped


def advance_population_by_days(population: List[int], days: int) -> List[int]:
    """
    Decrements the counters of each lanternfish age group and adds the newborn fishes
    to their age group.
    """
    for day in range(days):
        breeding = population.pop(0)
        population[6] += breeding
        population.append(breeding)  # new lanternfish
    return population


if __name__ == '__main__':
    population = read_population_ages()
    population = advance_population_by_days(population, 80)

    print(f'Population after 80 days: {sum(population)}')

    population = advance_population_by_days(population, 256 - 80)
    print(f'Population after 256 days: {sum(population)}')
