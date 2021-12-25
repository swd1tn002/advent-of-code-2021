from cucumber import _move_east, _move_south, transpose, count_steps_until_stable


def test_transpose():
    floor = 'abc\ndef'
    assert transpose(floor) == 'ad\nbe\ncf'


def test_move_east_wraps_over():
    floor = '..>..>v.>'
    assert _move_east(floor) == '>..>.>v..'


def test_move_south_wraps_over():
    floor = transpose('..v>..v..v')
    assert _move_south(floor) == transpose('v.v>...v..')


def test_steps_to_freeze_example_data():
    floor = '''
        v...>>.vv>
        .vv>>.vv..
        >>.>v>...v
        >>v>>.>.v.
        v>v.vv.v..
        >.>>..v...
        .vv..>.>v.
        v.v..>>v.v
        ....v..v.>
        '''.strip().replace(' ', '')

    steps = count_steps_until_stable(floor)
    assert steps == 58
