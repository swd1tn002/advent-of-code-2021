from image_enhancement import *


def test_read_algorithm_and_image():
    algorithm, pixels = read_algorithm_and_image()

    assert algorithm[:6] == '111010'
    assert len(algorithm) == 512
    assert pixels[(0, 0)] == '0'
    assert pixels[(1, 1)] == '1'


def test_pixel_to_binary():
    pixels = {
        (0, 0): '1',
        (1, 0): '0',
        (2, 0): '0',
        (0, 1): '1',
        (1, 1): '1',
        (2, 1): '0',
        (0, 2): '0',
        (1, 2): '0',
        (2, 2): '1',
    }
    binary = pixel_to_binary(pixels, Pixel(1, 1), '0')
    assert binary == '100110001'
