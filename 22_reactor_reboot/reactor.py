import re
from collections import namedtuple
from typing import List

import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


def read_cuboids(filename=INPUT_FILE) -> List['Cuboid']:
    """
    The reactor core is made up of a large 3-dimensional grid made up entirely of cubes,
    one cube per integer 3-dimensional coordinate (x,y,z). Each cube can be either on or
    off; at the start of the reboot process, they are all off.

    To reboot the reactor, you just need to set all of the cubes to either on or off by
    following a list of reboot steps (your puzzle input). Each step specifies a cuboid
    (the set of all cubes that have coordinates which fall within ranges for x, y, and z)
    and whether to turn all of the cubes in that cuboid on or off.
    """
    with open(filename) as file:
        puzzle_input = file.read().split('\n')

    return [parse_cuboid(line) for line in puzzle_input]


def parse_cuboid(line: str) -> 'Cuboid':
    """
    Parses the given string and returns a Cuboid object. For example:
    "on x=10..12,y=10..12,z=10..12" => Cuboid(Coord(10, 10, 10), Coord(13, 13, 13)).

    As the end coordinates in the puzzle input are inclusive, we add +1 to each
    dimension so we can use exclusive upper limits from now on.
    """
    number = r'(\-{0,1}\d+)'
    x0, x1, y0, y1, z0, z1 = [int(n) for n in re.findall(number, line)]

    value = ('on' == line[:2])

    return Cuboid(Coord(x0, y0, z0), Coord(x1+1, y1+1, z1+1), value)


Coord = namedtuple('Coord', 'x y z')


class Cuboid:
    def __init__(self, c0: Coord, c1: Coord, value: bool):
        self.c0 = c0
        self.c1 = c1
        self.value = value

    def __repr__(self) -> str:
        return f'Cuboid {self.c0} -> {self.c1} is {self.value}'

    def __eq__(self, __o: object) -> bool:
        return type(self) == type(__o) and repr(self) == repr(__o)

    def size(self) -> int:
        """
        Calculates the size of this Cuboid.
        """
        x0, y0, z0 = self.c0
        x1, y1, z1 = self.c1
        return (x1-x0) * (y1-y0) * (z1-z0)

    def is_inside(self, other: 'Cuboid') -> bool:
        """
        Returns True if this Cuboid is fully inside the given one.
        """
        return self.c0.x >= other.c0.x and self.c1.x <= other.c1.x and \
            self.c0.y >= other.c0.y and self.c1.y <= other.c1.y and \
            self.c0.z >= other.c0.z and self.c1.z <= other.c1.z

    def overlaps(self, other: 'Cuboid') -> bool:
        """
        Returns True if the given Cuboid has any overlapping lights with this one.
        """
        min_x1, max_x1 = self.c0.x, self.c1.x
        min_x2, max_x2 = other.c0.x, other.c1.x
        min_y1, max_y1 = self.c0.y, self.c1.y
        min_y2, max_y2 = other.c0.y, other.c1.y
        min_z1, max_z1 = self.c0.z, self.c1.z
        min_z2, max_z2 = other.c0.z, other.c1.z

        if min_x1 >= max_x2:
            return False
        if max_x1 <= min_x2:
            return False
        if min_y1 >= max_y2:
            return False
        if max_y1 <= min_y2:
            return False
        if min_z1 >= max_z2:
            return False
        if max_z1 <= min_z2:
            return False
        return True

    def explode_with(self, other: 'Cuboid') -> List['Cuboid']:
        """
        Splits the two Cuboids into max 27 new ones. The given Cuboids value 
        takes higher priority when determining the value for the new Cuboid.

        Returns two lists: first with new Cuboids from this one and the 
        second with new Cuboids from the other.
        """
        corners = (self.c0, self.c1, other.c0, other.c1)
        x_values = sorted([c.x for c in corners])
        y_values = sorted([c.y for c in corners])
        z_values = sorted([c.z for c in corners])

        split0: List['Cuboid'] = []
        split1: List['Cuboid'] = []

        if self.is_inside(other):
            # Just forget about this and use the other Cuboid if this is inside the other
            return [], [other]

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    c0 = Coord(x_values[i], y_values[j], z_values[k])
                    c1 = Coord(x_values[i+1], y_values[j+1], z_values[k+1])
                    r = Cuboid(c0, c1, None)
                    if r.size() == 0:
                        # Ignore cuboids with size 0
                        pass
                    elif r.overlaps(other):
                        r.value = other.value
                        split1.append(r)
                    elif r.overlaps(self):
                        r.value = self.value
                        split0.append(r)
                    else:
                        # The new Cuboid is outside the boundaries of both original Cuboids
                        pass

        return split0, split1


if __name__ == '__main__':
    cuboids: List[Cuboid] = read_cuboids()

    # Apply all cuboids in the steps. In case of overlapping cuboids, split them into non-overlapping
    # parts until no overlapping Cuboids exist.
    i = 0
    while i < len(cuboids):
        j = i + 1

        while j < len(cuboids):
            cube_i = cuboids[i]
            cube_j = cuboids[j]

            if cube_i.overlaps(cube_j):
                # Replace both cuboids with equal but not overlapping smaller cuboids.
                # Overlapping areas from the cube_i are cut out, as j formed after a later step:
                cuboids_i, cuboids_j = cube_i.explode_with(cube_j)

                # As j > i, always replace the latter ones first to avoid shifting their indices
                cuboids[j:j+1] = cuboids_j
                cuboids[i:i+1] = cuboids_i

                if len(cuboids_i) == 0:
                    # cube_i was completely removed. Start comparing to the new cube_i value
                    # from the cuboid right after it:
                    j = i + 1
            j += 1
        i += 1

    total = sum((cube.size() for cube in cuboids if cube.value))

    # Correct answer: 1134088247046731
    print(f'Part 2: In total {total} lights are on')
