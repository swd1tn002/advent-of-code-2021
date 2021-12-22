from reactor import Cuboid, Coord, parse_cuboid


def test_overlapping_one_inside_other():
    r0 = Cuboid(Coord(0, 0, 0), Coord(10, 10, 10), False)
    r1 = Cuboid(Coord(1, 1, 1), Coord(2, 2, 2), True)

    assert r0.overlaps(r1)
    assert r1.overlaps(r0)

    assert r1.is_inside(r0)
    assert not r0.is_inside(r1)


def test_overlapping_one_next_to_other():
    c0 = Cuboid(Coord(0, 0, 0), Coord(10, 10, 10), False)
    c1 = Cuboid(Coord(11, 0, 0), Coord(20, 0, 0), True)

    assert not c0.overlaps(c1)
    assert not c1.overlaps(c0)


def test_parse_cuboid():
    cuboid = parse_cuboid("on x=10..12,y=10..12,z=10..12")
    assert cuboid == Cuboid(Coord(10, 10, 10), Coord(13, 13, 13), True)


def test_size():
    """
    x=10..12,y=10..12,z=10..12 turns on a 3x3x3 cuboid consisting of 27 cubes.
    As we count with exclusive and not inclusive upper limits, the end coordinates
    are incremented by one.
    """
    c = Cuboid(Coord(10, 10, 10), Coord(12 + 1, 12 + 1, 12 + 1), False)
    assert c.size() == 27
