from dive_with_aim import dive_with_aim


def test_dive_with_aim():
    horizontal, depth = dive_with_aim([
        ('forward', 5),
        ('down', 5),
        ('forward', 8),
        ('up', 3),
        ('down', 8),
        ('forward', 2)
    ])
    assert horizontal == 15
    assert depth == 60
