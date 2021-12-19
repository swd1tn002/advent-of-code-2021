from typing import Dict, List, Tuple
from math import sqrt
import json
import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

"""
The beacons float motionless in the water; they're designed to maintain
the same position for long periods of time. Each beacon has x, y and z coordinates.
"""
Beacon = List[int]


def read_puzzle_input(filename=INPUT_FILE) -> List['Scanner']:
    """
    The submarine has automatically summarized the relative positions of beacons 
    detected by each scanner (your puzzle input).
    """
    scanners = []
    with open(filename) as file:
        chunks = file.read().split('\n\n')

        for i, chunk in enumerate(chunks):
            beacons = []
            for line in chunk.split('\n')[1:]:
                beacons.append([int(i) for i in line.split(',')])

            scanners.append(Scanner(i, beacons))

    return scanners


def distance(b1: Beacon, b2: Beacon) -> float:
    """
    Calculates the 3D distance of two beacons.
    """
    x1, y1, z1 = b1
    x2, y2, z2 = b2
    return sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)


class Scanner:
    """
    The beacons and scanners float motionless in the water; they're designed to maintain
    the same position for long periods of time. Each scanner is capable of detecting all
    beacons in a large cube centered on the scanner; beacons that are at most 1000 units
    away from the scanner in each of the three axes (x, y, and z) have their precise 
    position determined relative to the scanner. However, scanners cannot detect other scanners.

    Unfortunately, while each scanner can report the positions of all detected beacons 
    relative to itself, the scanners do not know their own position. You'll need to
    determine the positions of the beacons and scanners yourself.
    """

    def __init__(self, id: int, beacons: List[Beacon]):
        self.id = id
        self.beacons = beacons
        self.coordinates = [0, 0, 0]
        self.distances = self._map_distances(beacons)

    def __repr__(self) -> str:
        return f'{self.id} {self.coordinates}'

    def _map_distances(self, beacons) -> Dict:
        return {
            str(beacon): {distance(beacon, other)
                          for other in beacons}
            for beacon in beacons
        }

    def find_matching_beacons(self, other: 'Scanner') -> Tuple[List[Beacon]]:
        """
        The scanners and beacons map a single contiguous 3d region. This region can be
        reconstructed by finding pairs of scanners that have overlapping detection 
        regions such that there are at least 12 beacons that both scanners detect within
        the overlap. By establishing 12 common beacons, you can precisely determine where
        the scanners are relative to each other, allowing you to reconstruct the beacon 
        map one scanner at a time.

        If this Scanner and the given scanner detect overlapping beacons, this method
        returns two lists of Beacons in the order that they correspond to each other, but
        with their different orientations and relative positions.
        """
        group_a, group_b = [], []

        for beacon0, distance_set0 in self.distances.items():
            for beacon1, distance_set1 in other.distances.items():
                # If two beacons detected by two scanners have equal distances to 11
                # other beacons, they are determined to actually be the same beacon.
                if len(distance_set0 & distance_set1) >= 12:
                    group_a.append(json.loads(beacon0))
                    group_b.append(json.loads(beacon1))

        return [group_a, group_b]

    def transform(self, rotation, alignment: Beacon) -> None:
        """
        Transforms all detected beacon coordinates to the given rotation
        and relative to the given center alignment, that is also the
        position of this Scanner in the 3d space.
        """
        self.coordinates = alignment

        self.beacons = [rotation(*b) for b in self.beacons]
        self.beacons = [add_coord(alignment, b) for b in self.beacons]
        self.distances = self._map_distances(self.beacons)


def add_coord(c1: Beacon, c2: Beacon) -> Beacon:
    return [c1[i] + c2[i] for i in range(3)]


def subtract_coord(c1: Beacon, c2: Beacon) -> Beacon:
    return [c1[i] - c2[i] for i in range(3)]


def rotations():
    """
    "Unfortunately, there's a second problem: the scanners also don't know their 
    rotation or facing direction."

    This function generates functions for transforming a coordinate to all possible
    rotations and facing directions.
    """
    directions = [
        [1, 1, 1], [-1, -1, -1], [-1, 1, 1], [1, -1, 1],
        [1, 1, -1], [-1, -1, 1], [1, -1, -1], [-1, 1, -1]
    ]
    for a, b, c in directions:
        yield lambda x, y, z: [a * x, b * y, c * z]
        yield lambda x, y, z: [a * x, b * z, c * y]
        yield lambda x, y, z: [a * y, b * x, c * z]
        yield lambda x, y, z: [a * y, b * z, c * x]
        yield lambda x, y, z: [a * z, b * x, c * y]
        yield lambda x, y, z: [a * z, b * y, c * x]


def find_transformation(mesh1: List[Beacon], mesh2: List[Beacon]) -> Tuple:
    """
    Returns a rotation and alignment function that converts mesh 2 into mesh 1.
    Given meshes need to have the exact same Beacons in the same order, but in
    different orientation and relative position.

    Returns a function for rotating and a Beacon vector for aligning the second mesh.
    """
    for rotation in rotations():
        rotated = [rotation(*beacon) for beacon in mesh2]

        # A set of vectors between the mesh 1 and mesh 2 points.
        # If the meshes are in the same orientation, each vector is identical.
        vectors = {str(subtract_coord(mesh1[i], rotated[i]))
                   for i in range(len(rotated))}

        if len(vectors) == 1:
            return rotation, subtract_coord(mesh1[1], rotated[1])
    return None, None


def manhattan_distance(a: Scanner, b: Scanner) -> int:
    """
    Sometimes, it's a good idea to appreciate just how big the ocean is. Using the 
    Manhattan distance, how far apart do the scanners get?
    """
    return sum(abs(a.coordinates[i] - b.coordinates[i]) for i in range(3))


def align_scanners(scanners: List[Scanner]) -> List[Scanner]:
    """
    Aligns the given list of scanners by rotating and adjusting the coordinates
    of given scanners and their beacons to match the orientation of the first
    scanner on the list.

    Returns the given list of scanners after being aligned.
    """
    first, *unaligned = scanners

    aligned: List[Scanner] = [first]

    while unaligned:
        for scanner in aligned:
            for other in unaligned:
                # Do the detected beacons by the scanners overlap?
                a, b = scanner.find_matching_beacons(other)

                if a and b:
                    rotation, alignment = find_transformation(a, b)
                    other.transform(rotation, alignment)

                    print(f'Scanners {scanner} and {other} overlap!')

                    unaligned.remove(other)
                    aligned.append(other)
    return scanners


if __name__ == '__main__':
    scanners = read_puzzle_input()

    scanners = align_scanners(scanners)

    # Part 1: Assemble the full map of beacons. How many beacons are there?
    all_beacons = {str(b) for scanner in scanners for b in scanner.beacons}

    print(f'Part 1: there are {len(all_beacons)} beacons')

    # Part 2: What is the largest Manhattan distance between any two scanners?
    max_distance = max(((manhattan_distance(a, b), a, b)
                       for a in scanners for b in scanners), key=lambda x: x[0])

    print(f'Part 2: the maximum distance is {max_distance[0]}')
    print(f'Part 2: Scanners {max_distance[1].id} and {max_distance[2].id}')
