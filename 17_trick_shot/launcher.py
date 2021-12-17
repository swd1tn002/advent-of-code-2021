from typing import List, Tuple
import os
import re

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

Area = Tuple['Position']


class Velocity:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def next(self) -> 'Velocity':
        """
        Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it
        decreases by 1 if it is greater than 0, increases by 1 if it is less than 0, or
        does not change if it is already 0. Due to gravity, the probe's y velocity decreases by 1.
        """
        return Velocity(max((self.x - 1, 0)), self.y - 1)


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def in_area(self, area: Area) -> bool:
        x_bounds = [pos.x for pos in area]
        y_bounds = [pos.y for pos in area]
        return min(x_bounds) <= self.x <= max(x_bounds) and min(y_bounds) <= self.y <= max(y_bounds)

    def apply(self, velocity: Velocity) -> 'Position':
        """
        On each step, these changes occur in the following order:

        The probe's x position increases by its x velocity.
        The probe's y position increases by its y velocity.
        """
        return Position(self.x + velocity.x, self.y + velocity.y)


def read_puzzle_input(filename=INPUT_FILE) -> Area:
    """
    Converts text such as "target area: x=20..30, y=-10..-5" int a tuple of
    Positions such as (Position(20, -10), Position(30, -5)).
    """
    num_pattern = r'(\-{0,1}\d+)'
    with open(filename) as file:
        text = file.read()
        x0, x1, y0, y1 = [int(n) for n in re.findall(num_pattern, text)]
        return (Position(x0, y0), Position(x1, y1))


def trajectory_to_area(velocity: Velocity, area: Area) -> List[Position]:
    """
    Returns a path leading from (0, 0) to the given are with given initial
    velocity, if on exists. If no path can be built, returns None.
    """
    position = Position(0, 0)
    path: List[Position] = [position]

    while is_moving_towards_target(position, velocity, area):
        position = position.apply(velocity)
        velocity = velocity.next()
        path.append(position)

        if position.in_area(area):
            return path

    return None


def is_moving_towards_target(position: Position, velocity: Velocity, target_area: Area) -> bool:
    """
    Detects if a projectile is moving towards the given area.
    """
    max_x = max(pos.x for pos in target_area)
    min_x = min(pos.x for pos in target_area)
    min_y = min(pos.y for pos in target_area)

    too_low = position.y < min_y
    too_far = position.x > max_x
    if too_low or too_far:
        return False

    return velocity.x > 0 or (velocity.x == 0 and min_x <= position.x <= max_x)


if __name__ == '__main__':
    target_area: Area = read_puzzle_input()

    max_x = max(pos.x for pos in target_area)
    min_y = min(pos.y for pos in target_area)

    # Anything above max_x won't even start coming down, so it is chosen as the upper limit for y.
    # Anything above max_x will go past the goal in the first step, so it is the upper limit for x.
    attempts: List[Velocity] = [
        Velocity(x, y) for y in range(min_y, max_x) for x in range(1, max_x+1)
    ]

    trajectories = list(filter(None, (trajectory_to_area(velocity, target_area)
                                      for velocity in attempts)))

    max_y = max(pos.y for t in trajectories for pos in t)

    print(f'Part 1: maximum y value is {max_y}')
    print(f'Part 2: total amount of projectiles is {len(trajectories)}')
