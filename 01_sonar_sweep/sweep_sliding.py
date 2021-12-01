from sweep import sonar_sweep, count_increasing_numbers


def group_measurements(data):
    """consider sums of a three-measurement sliding window"""
    result = []

    for i in range(0, len(data) - 2):
        sum_of_three = sum(data[i:i+3])
        result.append(sum_of_three)

    return result


if __name__ == '__main__':
    """Your goal now is to count the number of times the sum of measurements 
    in this sliding window increases from the previous sum."""

    depths = sonar_sweep()
    sliding_depths = group_measurements(depths)
    increased = count_increasing_numbers(sliding_depths)

    print(f'Depth increased {increased} times!')
