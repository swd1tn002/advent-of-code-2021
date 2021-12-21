from beacon_scanner import *
import os
from pytest import fixture

TEST_INPUT_FILE = os.path.join(os.path.dirname(__file__), 'test_input.txt')


@fixture
def scanners() -> List[Scanner]:
    return read_puzzle_input(TEST_INPUT_FILE)


def test_reading_input():
    scanners = read_puzzle_input(TEST_INPUT_FILE)

    assert len(scanners) == 5
    assert scanners[0].coordinates == (0, 0, 0)


def test_overlapping_scanners(scanners: List[Scanner]):
    """
    Scanners 0 and 1 have overlapping detection cubes;
    """
    beacons0, beacons1 = scanners[0].find_matching_beacons(scanners[1])
    assert len(beacons0) == len(beacons1) == 12

    """
    the 12 beacons they both detect (relative to scanner 0) are at the following coordinates:
    -618,-824,-621  ... -485,-357,347
    
    These same 12 beacons (in the same order) but from the perspective of scanner 1 are:
    686, 422, 578  ...  553, 889, -390
    """

    assert (-618, -824, -621) in beacons0
    assert (686, 422, 578) in beacons1

    assert (-485, -357, 347) in beacons0
    assert (553, 889, -390) in beacons1


def test_transform_scanner_and_beacons(scanners: List[Scanner]):
    """
    ...Because of this, scanner 1 must be at 68, -1246, -43 (relative to scanner 0).
    """
    s0, s1, *rest = scanners
    beacons0, beacons1 = s0.find_matching_beacons(s1)

    rotation, alignment = find_transformation(beacons0, beacons1)
    assert alignment == (68, -1246, -43)

    # Change the orientation and alignment of scanner 1 to match scanner 0:
    s1.transform(rotation, alignment)

    # After transforming, the sensors have 12 exactly same beacons in their view
    set0 = set(map(str, s0.beacons))
    set1 = set(map(str, s1.beacons))
    assert len(set0 & set1) == 12


def test_align_scanners(scanners: List[Scanner]):
    s0, s1, s2, s3, s4 = align_scanners(scanners)

    # ...scanner 1 must be at 68,-1246,-43 (relative to scanner 0).
    assert s1.coordinates == (68, -1246, -43)

    # ...scanner 2 must be at 1105,-1205,1229
    assert s2.coordinates == (1105, -1205, 1229)

    # ...scanner 3 must be at -92,-2380,-20
    assert s3.coordinates == (-92, -2380, -20)

    # ...scanner 4 is at -20,-1133,1061
    assert s4.coordinates == (-20, -1133, 1061)
