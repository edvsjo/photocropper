"""A simple product finder that assumes a single-colored background"""
from typing import Optional
import numpy as np
from PIL import Image

from cropper import Rectangle


def uniform_background_product_finder(image: Image) -> Rectangle:
    """A product finder that assumes there is a uniform, single-colored
    background behind the product. Uses this to find and return the
    smallest rectangle containing the product.
    """
    greyscale_image = _greyscale(image)

    background_color = _most_common_color(greyscale_image)

    left = _length_left_margin(greyscale_image, background_color)
    upper = _length_top_margin(greyscale_image, background_color)
    right = (len(greyscale_image[0]) -
             _length_right_margin(greyscale_image, background_color))
    lower = (len(greyscale_image) -
             _length_bottom_margin(greyscale_image, background_color))

    return Rectangle(left, upper, right, lower)


def _greyscale(image: Image):
    image_data = np.asarray(image)
    return np.mean(image_data, axis=2)


def _most_common_color(greyscale_image: np.ndarray):
    colors, counts = np.unique(greyscale_image, return_counts=True)
    return colors[np.argmax(counts)]


def _length_top_margin(greyscale_image: np.ndarray, background_color) -> int:
    """ How many rows at the top have solely the `background_color`? """
    def contains_other_than_background_color(row) -> bool:
        return not _nearly_only_contains(background_color, row)

    first_non_background_row = _index_of_first_occurence(
        contains_other_than_background_color, greyscale_image
    )

    if first_non_background_row is not None:
        return first_non_background_row
    return len(greyscale_image)


def _length_bottom_margin(greyscale_image: np.ndarray, background_color):
    """ How many rows at the bottom have solely the `background_color`? """
    return _length_top_margin(np.flip(greyscale_image), background_color)


def _length_left_margin(greyscale_image: np.ndarray, background_color):
    """ How many columns at the left have solely the `background_color`? """
    return _length_top_margin(np.transpose(greyscale_image), background_color)


def _length_right_margin(greyscale_image: np.ndarray, background_color):
    """ How many columns at the right have solely the `background_color`? """
    return _length_bottom_margin(np.transpose(greyscale_image), background_color)


def _index_of_first_occurence(condition, array) -> Optional[int]:
    for index, value in enumerate(array):
        if condition(value):
            return index
    return None


def _nearly_only_contains(value, array) -> bool:
    for element in array:
        # if element != value:
        if not (element > value-20 and element < value+20):
            return False
    return True
