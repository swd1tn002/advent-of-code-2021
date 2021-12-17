from launcher import *


def test_read_puzzle_input():
    area = read_puzzle_input()

    # target area: x = 265..287, y = -103..-58
    assert area[0].x == 265
    assert area[0].y == -103
    assert area[1].x == 287
    assert area[1].y == -58


def test_aoc_example_1():
    target = (Position(20, -10), Position(30, -5))
    velocity = Velocity(7, 2)

    trajectory = trajectory_to_area(velocity, target)

    assert len(trajectory) == 8

    # highest point
    assert trajectory[2].x == 13
    assert trajectory[2].y == 3


def test_trajectory_through_target_area():
    # One initial velocity that doesn't cause the probe to be within
    # the target area after any step is 17, -4.
    # The probe appears to pass through the target area, but is never
    # within it after any step.
    target = (Position(20, -10), Position(30, -5))
    velocity = Velocity(17, 4)

    trajectory = trajectory_to_area(velocity, target)

    assert trajectory == None
