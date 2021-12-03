import os
INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


def convert_to_bits(line: str) -> list[int]:
    """
    Takes a str with numbers 0 and 1 and returns them as a list of ints.
    """
    return list(map(int, line))


def read_report():
    """
    The diagnostic report (your puzzle input) consists of a list of binary numbers which,
    when decoded properly, can tell you many useful things about the conditions of the
    submarine. The first parameter to check is the power consumption.
    """
    with open(INPUT_FILE) as file:
        lines = file.read().splitlines()

    return list(map(convert_to_bits, lines))


def most_common_bit(bits: list[int], tie=1) -> int:
    """
    Returns the most common bit in given list. In case of a tie, returns 1.
    """
    as_list = list(bits)
    zeros = as_list.count(0)
    ones = as_list.count(1)

    return 0 if zeros > ones else 1


def find_most_common_bits(data: list, tie=1) -> list[int]:
    """
    Returns a list of most common bits in each position. In case of a tie, returns 1
    """
    zipped = zip(*data)
    common_bits = map(most_common_bit, zipped)
    return list(common_bits)


def invert_bits(bits):
    """
    Returns a new list with ones as zeros and vice versa
    """
    return list(map(lambda bit: bit ^ 1, bits))  # bitwise xor


def bits_to_decimal(bits: list[int]) -> int:
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