from amphipod import move_amphipods_home, is_completed
from pytest import fixture

test_input = """
#############
#.A.B.D.C...#
###.#.#.#.###
  #A#B#C#D#
  #########
"""


@fixture
def test_puzzle():
    return [list(row) for row in test_input.strip().split('\n')]


def test_moving_home_with_costs(test_puzzle):
    solution, cost = move_amphipods_home(test_puzzle, 0)

    assert is_completed(solution)
    assert cost == 4_222  # 3*1 + 2*10 + 2*100 + 4*1000
