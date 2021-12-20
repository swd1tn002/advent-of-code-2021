from typing import Tuple, Dict, List
from collections import namedtuple
import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')

Pixel = namedtuple('Pixel', 'x y')


def read_algorithm_and_image(filename=INPUT_FILE) -> Tuple:
    """
    Reads the puzzle input, where the first section is the image enhancement algorithm.
    The second section is the input image, a two-dimensional grid of light pixels(#) and dark pixels (.).

    Returns the algorithm and a dictionary of pixels and their values converted to 1 and 0.
    """
    with open(filename) as file:
        puzzle_input = file.read().replace('#', '1').replace('.', '0')

    algorithm, input_image = puzzle_input.split('\n\n')

    pixels: Dict[Tuple, str] = {}
    for y, row in enumerate(input_image.split('\n')):
        for x, char in enumerate(row):
            pixels[Pixel(x, y)] = char

    return algorithm, pixels


def print_image(pixels: Dict[Pixel, str]):
    """
    Prints the given image as '#' and '.', as in the puzzle examples.
    """
    x_range = [p.x for p in pixels.keys()]
    y_range = [p.y for p in pixels.keys()]
    for y in range(min(y_range), max(y_range) + 1):
        for x in range(min(x_range), max(x_range) + 1):
            print(pixels.get(Pixel(x, y), '0').replace(
                '0', '.').replace('1', '#'), end='')
        print()
    print()


def enhance_image(original: Dict[Pixel, str], algorithm: str, infinity: str) -> Dict[Pixel, str]:
    """
    The image enhancement algorithm describes how to enhance an image by simultaneously converting
    all pixels in the input image into an output image. Each pixel of the output image is determined
    by looking at a 3x3 square of pixels centered on the corresponding input image pixel.

    Through advances in imaging technology, the images being operated on here are infinite in size.
    Every pixel of the infinite output image needs to be calculated exactly based on the relevant 
    pixels of the input image.
    """
    x_range = {p.x for p in original.keys()}
    y_range = {p.y for p in original.keys()}

    output: Dict[Pixel, str] = {}
    for y in range(min(y_range) - 1, max(y_range) + 2):
        for x in range(min(x_range) - 1, max(x_range) + 2):
            pixel = Pixel(x, y)
            binary = pixel_to_binary(original, pixel, infinity)
            output[pixel] = algorithm[int(binary, 2)]
    return output


def pixel_to_binary(image: Dict[Pixel, str], pixel: Pixel, infinity: str) -> str:
    """
    To determine the value of the pixel at (5,10) in the output image, nine pixels from the input image 
    need to be considered: (4,9), (4,10), (4,11), (5,9), (5,10), (5,11), (6,9), (6,10), and (6,11). 
    These nine input pixels are combined into a single binary number that is used as an index in the
    image enhancement algorithm string.
    """
    binary = ''
    _x, _y = pixel
    for y in (_y - 1, _y, _y + 1):
        for x in (_x - 1, _x, _x + 1):
            binary += image.get(Pixel(x, y), infinity)
    return binary


if __name__ == '__main__':
    algorithm, pixels = read_algorithm_and_image()

    print_image(pixels)

    """
    The small input image you have is only a small region of the actual infinite input image;
    the rest of the infinite image consists of dark pixels (which may turn bright when image is enhanced!)
    """
    infinity = '0'
    enhanced = pixels

    for i in range(50):
        enhanced = enhance_image(enhanced, algorithm, infinity)

        # Update the common value for all remaining infinite pixels outside the known area
        infinity = algorithm[int(infinity * 9, 2)]

        # Part 1: 5 065 is the correct answer
        # Part 2: 14 790 is the correct answer
        if infinity == '0':
            print(i + 1, len([e for e in enhanced.values()
                  if e == '1']), 'bright pixels')
        else:
            print(i + 1, 'Infinite bright pixels')

    print_image(enhanced)
