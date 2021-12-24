from typing import List, Dict, Tuple
from functools import lru_cache


# @lru_cache(maxsize=100_000)
def solver0(w, x, y, z):
    x = x * 0
    x = x + z
    x = x % 26
    z = z // 1
    x = x + 10
    x = int(x == w)
    x = int(x == 0)
    y = y * 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = y * 0
    y = y + w
    y = y + 12
    y = y * x
    z = z + y
    return w, x, y, z


# @lru_cache(maxsize=100_000)
def solver1(w, x, y, z):
    x = x * 0
    x = x + z
    x = x % 26
    z = z // 1
    x = x + 10
    x = int(x == w)
    x = int(x == 0)
    y = y * 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = y * 0
    y = y + w
    y = y + 10
    y = y * x
    z = z + y
    return w, x, y, z


# @lru_cache(maxsize=100_000)
def solver2(w, x, y, z):
    x = x * 0
    x = x + z
    x = x % 26
    z = z // 1
    x = x + 12
    x = int(x == w)
    x = int(x == 0)
    y = y * 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = y * 0
    y = y + w
    y = y + 8
    y = y * x
    z = z + y
    return w, x, y, z


# @lru_cache(maxsize=100_000)
def solver3(w, x, y, z):
    x = x * 0
    x = x + z
    x = x % 26
    z = z // 1
    x = x + 11
    x = int(x == w)
    x = int(x == 0)
    y = y * 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = y * 0
    y = y + w
    y = y + 4
    y = y * x
    z = z + y
    return w, x, y, z


# @lru_cache(maxsize=100_000)
def solver4(w, x, y, z):
    x = x * 0
    x = x + z
    x = x % 26
    z = z // 26
    x = x + 0
    x = int(x == w)
    x = int(x == 0)
    y = y * 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = y * 0
    y = y + w
    y = y + 3
    y = y * x
    z = z + y
    return w, x, y, z


# @lru_cache(maxsize=100_000)
def solver5(w, x, y, z):
    x = x * 0
    x = x + z
    x = x % 26
    z = z // 1
    x = x + 15
    x = int(x == w)
    x = int(x == 0)
    y = y * 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = y * 0
    y = y + w
    y = y + 10
    y = y * x
    z = z + y
    return w, x, y, z


# @lru_cache(maxsize=100_000)
def solver6(w, x, y, z):
    x = x * 0
    x = x + z
    x = x % 26
    z = z // 1
    x = x + 13
    x = int(x == w)
    x = int(x == 0)
    y = y * 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = y * 0
    y = y + w
    y = y + 6
    y = y * x
    z = z + y
    return w, x, y, z


# @lru_cache(maxsize=100_000)
def solver7(w, x, y, z):
    x = x * 0
    x = x + z
    x = x % 26
    z = z // 26
    x = x + -12
    x = int(x == w)
    x = int(x == 0)
    y = y * 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = y * 0
    y = y + w
    y = y + 13
    y = y * x
    z = z + y
    return w, x, y, z


# @lru_cache(maxsize=100_000)
def solver8(w, x, y, z):
    x = x * 0
    x = x + z
    x = x % 26
    z = z // 26
    x = x + -15
    x = int(x == w)
    x = int(x == 0)
    y = y * 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = y * 0
    y = y + w
    y = y + 8
    y = y * x
    z = z + y
    return w, x, y, z


# @lru_cache(maxsize=100_000)
def solver9(w, x, y, z):
    x = x * 0
    x = x + z
    x = x % 26
    z = z // 26
    x = x + -15
    x = int(x == w)
    x = int(x == 0)
    y = y * 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = y * 0
    y = y + w
    y = y + 1
    y = y * x
    z = z + y
    return w, x, y, z


# @lru_cache(maxsize=100_000)
def solver10(w, x, y, z):
    x = x * 0
    x = x + z
    x = x % 26
    z = z // 26
    x = x + -4
    x = int(x == w)
    x = int(x == 0)
    y = y * 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = y * 0
    y = y + w
    y = y + 7
    y = y * x
    z = z + y
    return w, x, y, z


# @lru_cache(maxsize=100_000)
def solver11(w, x, y, z):
    x = x * 0
    x = x + z
    x = x % 26
    z = z // 1
    x = x + 10
    x = int(x == w)
    x = int(x == 0)
    y = y * 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = y * 0
    y = y + w
    y = y + 6
    y = y * x
    z = z + y
    return w, x, y, z


# @lru_cache(maxsize=100_000)
def solver12(w, x, y, z):
    x = x * 0
    x = x + z
    x = x % 26
    z = z // 26
    x = x + -5
    x = int(x == w)
    x = int(x == 0)
    y = y * 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = y * 0
    y = y + w
    y = y + 9
    y = y * x
    z = z + y
    return w, x, y, z


# @lru_cache(maxsize=100_000)
def solver13(w, x, y, z):
    x = x * 0
    x = x + z
    x = x % 26
    z = z // 26
    x = x + -12
    x = int(x == w)
    x = int(x == 0)
    y = y * 0
    y = y + 25
    y = y * x
    y = y + 1
    z = z * y
    y = y * 0
    y = y + w
    y = y + 9
    y = y * x
    z = z + y
    return w, x, y, z


solvers = (
    solver0,
    solver1,
    solver2,
    solver3,
    solver4,
    solver5,
    solver6,
    solver7,
    solver8,
    solver9,
    solver10,
    solver11,
    solver12,
    solver13
)


@lru_cache(maxsize=100_000)
def solve(x, y, z, funcs: Tuple):
    if not funcs:
        return z == 0, ''

    func, *rest = funcs

    for i in range(1, 10):
        _, _x, _y, _z = func(i, x, y, z)

        found, suffix = solve(_x, _y, _z, tuple(rest))

        if found:
            return True, str(i) + suffix

    return False, None


print(solve(x=0, y=0, z=0, funcs=solvers))

# if __name__ == '__main__':
#     # Split into sub programs which all use only one input value
#     blocks = lines.split('\ninp')
#     blocks = [blocks[0]] + ['inp' + block for block in blocks[1:]]

#     programs: List[ALU] = []

#     for block in blocks:
#         programs.append(ALU(block.split('\n')))

#     # Solve use the given programs recursively to find the highest input combination
#     # that is a valid serial number
#     solution = solve({'w': 0, 'x': 0, 'y': 0, 'z': 0}, programs)
#     print(solution)

#     # Start from 99999995597000
