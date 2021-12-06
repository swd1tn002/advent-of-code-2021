from lanternfish import read_population_ages, advance_population_by_days


def test_read_population_ages():
    population = read_population_ages()

    assert len(population) == 9

    assert all(count > 0 for count in population[1:6])
    assert population[7] == 0
    assert population[8] == 0


def test_advance_population_by_one_day():
    population = [1, 2, 3, 4, 0, 0, 0, 0, 0]

    advance_population_by_days(population, 1)

    assert population == [2, 3, 4, 0, 0, 0, 1, 0, 1]


def test_advance_population_by_multiple_days():
    population = [1, 2, 3, 4, 0, 0, 0, 0, 0]

    advance_population_by_days(population, 2)

    assert population == [3, 4, 0, 0, 0, 1, 2, 1, 2]
