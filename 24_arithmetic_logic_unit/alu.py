from typing import Tuple
from collections.abc import Callable
from functools import lru_cache
from monad import *

solvers = (solver0, solver1, solver2, solver3, solver4, solver5, solver6,
           solver7, solver8, solver9, solver10, solver11, solver12, solver13)


@lru_cache(maxsize=100_000)
def solve(x, y, z, funcs: Tuple[Callable], order: Tuple[int]):
    if not funcs:
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
