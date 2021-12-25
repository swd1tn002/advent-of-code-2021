from typing import Tuple
from collections.abc import Callable
from functools import lru_cache
from monad import *

# The MONAD program is split into 14 different steps, each of which consumes
# a single digit from the 14 digit serial numbers.
solvers = (solver0, solver1, solver2, solver3, solver4, solver5, solver6,
           solver7, solver8, solver9, solver10, solver11, solver12, solver13)


@lru_cache(maxsize=100_000)
def solve(x, y, z, funcs: Tuple[Callable], order: Tuple[int]) -> Tuple:
    """
    Applies depth-first-search to find the first sequence of numbers that, when given
    to the MONAD program, produce the z value of 0.

    The MONAD program is split into 14 steps, which each read one input parameter (w)
    and use three parameters from previous results (x, y and z).

    When all the parts of the MONAD (funcs) are consumed, this function determines if 
    the end value for `z` is 0 (a valid serial number). If so, `True` and the digits
    leading to the outcome are catenated and returned.
    """

    if not funcs:
        """
        **After MONAD has finished running all of its instructions, it will indicate that
        the model number was valid by leaving a 0 in variable z.**
        """
        return z == 0, ''

    func, *rest = funcs

    for i in order:
        _, _x, _y, _z = func(i, x, y, z)

        found, suffix = solve(_x, _y, _z, tuple(rest), order)

        if found:
            return True, str(i) + suffix

    return False, None


if __name__ == '__main__':
    # Part 1: What is the largest model number accepted by MONAD?
    descending = tuple(range(9, 0, -1))
    _, largest = solve(x=0, y=0, z=0, funcs=solvers, order=descending)

    if largest:
        print(f'The largest model number accepted by MONAD is {largest}')

    # Part 2: What is the smallest model number accepted by MONAD?
    ascending = tuple(range(1, 10))
    _, smallest = solve(x=0, y=0, z=0, funcs=solvers, order=ascending)

    if smallest:
        print(f'The smallest model number accepted by MONAD is {smallest}')
