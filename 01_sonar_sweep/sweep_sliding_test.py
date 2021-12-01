from sweep_sliding import group_measurements


def test_group_measurements_sums_each_three_numbers_in_row():
    nums = [0, 1, 2, 3, 4, 5]

    assert group_measurements(nums) == [3, 6, 9, 12]
