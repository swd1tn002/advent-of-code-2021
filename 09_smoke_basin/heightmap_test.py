from heightmap import Coord, parse_heightmap

test_input = ['2199943210',
              '3987894921',
              '9856789892',
              '8767896789',
              '9899965678']


def test_parse_heightmap():
    heightmap = parse_heightmap(test_input)

    assert heightmap[Coord(0, 0)] == 2
    assert heightmap[Coord(0, 1)] == 3
    assert heightmap[Coord(1, 0)] == 1
