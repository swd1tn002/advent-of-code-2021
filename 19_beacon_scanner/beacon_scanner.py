from typing import Dict, List
from puzzle_input import txt
from math import sqrt
import json


def distance(b1, b2) -> float:
    x1, y1, z1 = b1
    x2, y2, z2 = b2
    return sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)


class Scanner:
    def __init__(self, id, beacons):
        self.id = id
        self.beacons = beacons
        self.coordinates = [0, 0, 0]
        self.distances = self._map_distances(beacons)

    def __repr__(self) -> str:
        return f'{self.id} ({len(self.beacons)} beacons)'

    def _map_distances(self, beacons) -> Dict:
        return {
            str(beacon): {distance(beacon, other)
                          for other in beacons}
            for beacon in beacons
        }

    def find_matching_beacons(self, other: 'Scanner') -> List:
        group_a = []
        group_b = []
        for beacon0, distance_set0 in self.distances.items():
            for beacon1, distance_set1 in other.distances.items():
                # Find at least 12 overlapping distances to identify that the beacons are equal
                if len(distance_set0 & distance_set1) >= 12:
                    group_a.append(json.loads(beacon0))
                    group_b.append(json.loads(beacon1))
        return [group_a, group_b]

    def rotate_all(self, rotation):
        self.beacons = [rotation(*b) for b in self.beacons]

    def shift_position(self, vector):
        self.beacons = [[b[0]-vector[0], b[1]-vector[1],
                         b[2]-vector[2]] for b in self.beacons]


chunks = txt.split('\n\n')

scanners = []
for i, chunk in enumerate(chunks):
    beacons = []
    for line in chunk.split('\n')[1:]:
        beacons.append([int(i) for i in line.split(',')])

    scanners.append(Scanner(i, beacons))

print(scanners)


def vector(c1, c2) -> List:
    return [c1[i] - c2[i] for i in range(3)]


def rotators():
    yield lambda x, y, z: [x, y, z]
    yield lambda x, y, z: [x, z, y]
    yield lambda x, y, z: [y, x, z]
    yield lambda x, y, z: [y, z, x]
    yield lambda x, y, z: [z, x, y]
    yield lambda x, y, z: [z, y, x]

    yield lambda x, y, z: [-x, y, z]
    yield lambda x, y, z: [-x, z, y]
    yield lambda x, y, z: [y, -x, z]
    yield lambda x, y, z: [y, -z, x]
    yield lambda x, y, z: [z, -x, y]
    yield lambda x, y, z: [z, y, -x]

    yield lambda x, y, z: [x, -y, z]
    yield lambda x, y, z: [x, z, -y]
    yield lambda x, y, z: [-y, x, z]
    yield lambda x, y, z: [-y, z, x]
    yield lambda x, y, z: [z, x, -y]
    yield lambda x, y, z: [z, -y, x]

    yield lambda x, y, z: [x, y, -z]
    yield lambda x, y, z: [x, -z, y]
    yield lambda x, y, z: [y, x, -z]
    yield lambda x, y, z: [y, -z, x]
    yield lambda x, y, z: [-z, x, y]
    yield lambda x, y, z: [-z, y, x]

    yield lambda x, y, z: [x, -y, -z]
    yield lambda x, y, z: [x, -z, -y]
    yield lambda x, y, z: [-y, x, -z]
    yield lambda x, y, z: [-y, -z, x]
    yield lambda x, y, z: [-z, x, -y]
    yield lambda x, y, z: [-z, -y, x]

    yield lambda x, y, z: [-x, y, -z]
    yield lambda x, y, z: [-x, -z, y]
    yield lambda x, y, z: [y, -x, -z]
    yield lambda x, y, z: [y, -z, -x]
    yield lambda x, y, z: [-z, -x, y]
    yield lambda x, y, z: [-z, y, -x]

    yield lambda x, y, z: [-x, -y, z]
    yield lambda x, y, z: [-x, z, -y]
    yield lambda x, y, z: [-y, -x, z]
    yield lambda x, y, z: [-y, z, -x]
    yield lambda x, y, z: [z, -x, -y]
    yield lambda x, y, z: [z, -y, -x]


def find_rotation(mesh1, mesh2):
    """
    Returns a rotation function that converts mesh 2 into mesh 1.
    """
    for rotation in rotators():
        rotated = [rotation(*beacon) for beacon in mesh2]

        # A set of vectors between the mesh 1 and mesh 2 points.
        # If the meshes are in the same orientation, each vector is identical.
        vectors = {str(vector(mesh1[i], rotated[i]))
                   for i in range(len(rotated))}

        if len(vectors) == 1:
            return rotation
    raise Exception('No rotation found!')


# a, b = scanners[0].find_matching_beacons(scanners[1])

# print(a)
# print(b)

# rotation = find_rotation(a, b)
# print(f'Rotation between a and b is {rotation}')

# scanner1_position = vector(a[0], rotation(*b[0]))
# print(
#    f'Distance between scanners 0 and 1 is {scanner1_position} == 68,-1246,-43!!!')
# scanners[1].rotate_all(rotation)


mapped: List[Scanner] = [scanners[0]]
unmapped: List[Scanner] = scanners[1:]

while unmapped:
    for scanner_a in mapped:
        for scanner_b in unmapped:
            a, b = scanner_a.find_matching_beacons(scanner_b)

            # Do they have overlapping detection cubes?
            if len(a) >= 12:
                print(
                    f'Detection cubes of {scanner_a} and {scanner_b} overlap!')
                rotation = find_rotation(a, b)
                scanner_b.rotate_all(rotation)

                position_diff = vector(rotation(*b[0]), a[0])

                scanner_b.shift_position(position_diff)

                unmapped.remove(scanner_b)
                mapped.append(scanner_b)


beacons = {str(b) for scanner in scanners for beacon in scanner.beacons}

for scanner in mapped:
    print(scanner)
    beacons = beacons | {str(b) for b in scanner.beacons}
    for beacon in scanner.beacons:
        print(beacon)
    print()

print(len(beacons))