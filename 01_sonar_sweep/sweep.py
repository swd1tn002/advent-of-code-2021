import os
INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


def sonar_sweep():
    """
    Each line is a measurement of the sea floor depth as the sweep 
    looks further and further away from the submarine.
    """

    with open(INPUT_FILE) as file:
        lines = file.readlines()

    as_numbers = map(int, lines)
    return list(as_numbers)


def count_increasing_numbers(data):
    """
    Counts the number of times a depth measurement increases 
    from the previous measurement.
    """

    increased = 0

    for i in range(1, len(data)):
        if data[i] > data[i - 1]:
            increased += 1

    return increased


if __name__ == '__main__':
    depths = sonar_sweep()
    increased = count_increasing_numbers(depths)

    print(f'Depth increased {increased} times!')
