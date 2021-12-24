from alu import ALU


def test_negate():
    program = ['inp x', 'mul x -1']
    inp = [3]

    alu = ALU(program)
    result = alu.process({'w': 0, 'x': 0, 'y': 0, 'z': 0}, inp)
    assert result['x'] == -3


def test_three_times_larger():
    alu = ALU(['inp z', 'inp x', 'mul z 3', 'eql z x'])

    result_true = alu.process({'w': 0, 'x': 0, 'y': 0, 'z': 0}, [2, 6])
    assert result_true['z'] == 1

    result_false = alu.process({'w': 0, 'x': 0, 'y': 0, 'z': 0}, [2, 7])
    assert result_false['z'] == 0
