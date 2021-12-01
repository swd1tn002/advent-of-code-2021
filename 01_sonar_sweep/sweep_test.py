from sweep import count_increasing_numbers, sonar_sweep


def test_only_increasing_numbers():
    nums = [0, 1, 2, 3, 4, 5]

    assert count_increasing_numbers(nums) == 5


def test_only_decreasing_numbers():
    nums = [5, 4, 3, 2, 1, 0]

    assert count_increasing_numbers(nums) == 0


def test_equal_numbers():
    nums = [1, 2, 2, 3, 3, 5]

    assert count_increasing_numbers(nums) == 3


def test_mix_of_numbers():
    nums = [0, 100, 10, 200, 200, 500, 1]

    assert count_increasing_numbers(nums) == 3


def test_reading_file():
    results = sonar_sweep()

    assert len(results) == 2_000

    assert results[0] == 159
    assert results[-1] == 8_568
