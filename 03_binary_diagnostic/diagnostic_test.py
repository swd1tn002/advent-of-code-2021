from diagnostic import convert_to_bits, read_report, most_common_bit, find_most_common_bits, bits_to_decimal


def test_converting_string_to_bits():
    bits = convert_to_bits("11100")

    assert bits == [1, 1, 1, 0, 0]


def test_reading_report():
    report = read_report()

    assert report[0] == [1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0]
    assert report[-1] == [1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1]


def test_most_common_bit():
    bit_0 = most_common_bit([0, 0, 1])
    assert bit_0 == 0

    bit_1 = most_common_bit([1, 0, 1])
    assert bit_1 == 1


def test_find_most_common_bits():
    data = [[1, 1, 0], [1, 0, 0], [1, 0, 1]]

    result = find_most_common_bits(data)
    assert result == [1, 0, 0]


def test_bits_to_decimal():
    decimal = bits_to_decimal([1, 0, 1, 1, 0])

    assert decimal == 22
