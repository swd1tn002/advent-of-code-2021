import os
from typing import List
INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


def convert_to_bits(line: str) -> List[int]:
    """
    Takes a str with numbers 0 and 1 and returns them as a list of ints.
    """
    return list(map(int, line))


def read_report() -> List[List[int]]:
    """
    The diagnostic report (your puzzle input) consists of a list of binary numbers which,
    when decoded properly, can tell you many useful things about the conditions of the
    submarine. The first parameter to check is the power consumption.
    """
    with open(INPUT_FILE) as file:
        lines = file.read().splitlines()

    return list(map(convert_to_bits, lines))


def most_common_bit(bits: List[int]) -> int:
    """
    Returns the most common bit in given list. In case of a tie, returns 1.
    """
    as_list = list(bits)
    zeros = as_list.count(0)
    ones = as_list.count(1)

    return 0 if zeros > ones else 1


def find_most_common_bits(data: List[List[int]]) -> List[int]:
    """
    Returns a list of most common bits in each position across multiple bit lists.
    In case of a tie between ones and zeros, uses 1.
    """
    zipped = zip(*data)
    common_bits = map(most_common_bit, zipped)
    return list(common_bits)


def invert_bits(bits: List[int]) -> List[int]:
    """
    Returns a new list with ones as zeros and vice versa
    """
    def invert(bit): return bit ^ 1  # bitwise xor changes 0 to 1 and 1 to 0
    return list(map(invert, bits))


def bits_to_decimal(bits: List[int]) -> int:
    """
    Converts a list of int bits to a decimal number
    """
    binary_str = ''.join(map(str, bits))
    return int(binary_str, 2)


if __name__ == '__main__':
    report = read_report()
    gamma_bits = find_most_common_bits(report)
    epsilon_bits = invert_bits(gamma_bits)

    gamma_rate = bits_to_decimal(gamma_bits)
    epsilon_rate = bits_to_decimal(epsilon_bits)

    power_consumption = gamma_rate * epsilon_rate
    print(power_consumption)
