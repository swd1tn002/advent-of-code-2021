from alu_interpreter import alu_function


def test_converting_alu_to_python():
    lines = ['add z w',
             'mod z 2',
             'div w 2']

    converted = [line for line in alu_function(0, lines)]

    assert 'z += w' in converted[1]
    assert 'z %= 2' in converted[2]
    assert 'w //= 2' in converted[3]
    assert 'return w, x, y, z' in converted[4]
