from multiprocessing import Process
from typing import List, Dict, Tuple


class ALU:
    def __init__(self, instructions: List[str]):
        self.instructions = instructions

    def process(self, vars: Dict[str, int], inp: List[int]) -> Dict[str, int]:
        for instr in self.instructions:
            self._evaluate(instr, vars, inp)

        return vars

    def _evaluate(self, instr: str, vars: Dict[str, int], inp: List[int]):
        command, *params = instr.split()
        func = getattr(self, f'_{command}')
        func(vars, inp, params)

    def _inp(self, vars: Dict[str, int], inp: List[int], params: Tuple[str]):
        """
        inp a - Read an input value and write it to variable a.
        """
        vars[params[0]] = inp.pop(0)

    def _add(self, vars: Dict[str, int], inp: List[int], params: Tuple[str]):
        """
        add a b - Add the value of a to the value of b, then store the result in variable a.
        """
        a, b = params
        if b not in vars:
            b = int(b)
        else:
            b = vars[b]

        vars[a] += b

    def _mul(self, vars: Dict[str, int], inp: List[int], params: Tuple[str]):
        """
        mul a b - Multiply the value of a by the value of b, then store the result in variable a.
        """
        a, b = params
        if b not in vars:
            b = int(b)
        else:
            b = vars[b]
        vars[a] *= b

    def _div(self, vars: Dict[str, int], inp: List[int], params: Tuple[str]):
        """
        div a b - Divide the value of a by the value of b, truncate the result to an integer,
        then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
        """
        a, b = params
        if b not in vars:
            div = int(b)
        else:
            div = vars[b]
        vars[a] = vars[a] // div

    def _mod(self, vars: Dict[str, int], inp: List[int], params: Tuple[str]):
        """
        mod a b - Divide the value of a by the value of b, then store the remainder in variable a.
        """
        a, b = params
        if b not in vars:
            mod = int(b)
        else:
            mod = vars[b]
        vars[a] = vars[a] % mod

    def _eql(self, vars: Dict[str, int], inp: List[int], params: Tuple[str]):
        """
        eql a b - If the value of a and b are equal, then store the value 1 in variable a. 
        Otherwise, store the value 0 in variable a.
        """
        a, b = params
        if b not in vars:
            val = int(b)
        else:
            val = vars[b]
        vars[a] = int(vars[a] == val)


lines = """inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 12
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 10
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 8
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 4
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x 0
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 3
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 15
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 10
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 6
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -15
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 8
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -15
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 1
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -4
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 7
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 6
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -5
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 9
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 9
mul y x
add z y"""

counter = 0


def solve(vars: Dict[str, int], programs: List[ALU]):
    if not programs:
        global counter
        counter += 1
        if counter % 1_000 == 0:
            print(counter)

        """
        ...it will indicate that the model number was valid by leaving a 0 in variable z...
        """
        return vars['z'] == 0, ''

    p = programs[0]

    for n in range(9, 0, -1):
        result = p.process(vars.copy(), [n])
        found, suffix = solve(result, programs[1:])

        if found:
            return True, str(n) + suffix

    return False, None


if __name__ == '__main__':
    # Split into sub programs which all use only one input value
    blocks = lines.split('\ninp')
    blocks = [blocks[0]] + ['inp' + block for block in blocks[1:]]

    programs: List[ALU] = []

    for block in blocks:
        programs.append(ALU(block.split('\n')))

    # Solve use the given programs recursively to find the highest input combination
    # that is a valid serial number
    solution = solve({'w': 0, 'x': 0, 'y': 0, 'z': 0}, programs)
    print(solution)

    # Start from 99999995597000
