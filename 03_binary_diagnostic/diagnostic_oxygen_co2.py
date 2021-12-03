from typing import List
from diagnostic import read_report, find_most_common_bits, bits_to_decimal


def filter_by_common_bits_in_each_position(report: List[List[int]], most_common=True) -> List[int]:
    """
    Determine the most common value (0 or 1) in each bit position, and keep only the lists
    with either the most or least common bit in that position, determined by the most_common parameter.
    """
    filtered = report

    for bit_position in range(0, len(report[0])):
        common_bit = find_most_common_bits(filtered)[bit_position]

        # inverse the most common bit if searching for least common bit
        required_bit = common_bit if most_common else common_bit ^ 1

        filtered = list(filter(
            lambda x: x[bit_position] == required_bit, filtered))

        if len(filtered) == 1:
            break

    return filtered


def find_oxygen_generator_rating(report: List[List[int]]) -> int:
    """
    To find oxygen generator rating, determine the most common value (0 or 1) in
    each bit position, and keep only numbers with that bit in that position.
    If 0 and 1 are equally common, keep values with a 1 in the position being considered.
    """
    filtered = filter_by_common_bits_in_each_position(report, most_common=True)
    return bits_to_decimal(filtered[0])


def find_co2_generator_rating(report: List[List[int]]) -> int:
    """
    To determine the CO2 scrubber rating value keep only the numbers
    with least common bits in each position.
    """
    filtered = filter_by_common_bits_in_each_position(
        report, most_common=False)
    return bits_to_decimal(filtered[0])


if __name__ == '__main__':
    report = read_report()
    oxygen_rating = find_oxygen_generator_rating(report)
    co2_rating = find_co2_generator_rating(report)

    print(oxygen_rating * co2_rating)
