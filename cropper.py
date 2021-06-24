from typing import Callable
from PIL import Image

ASPECT_RATIO = 0.82690187431  # 1500 / 1814
WIDTH_PADDING = 100  # How much extra width to add to each side of the cropped image


class Rectangle:
    """A rectangle defined by its position and size."""
    def __init__(self, left, upper, right, lower):
        """
        Define a rectangle by:
        (left, upper) : the upper left corner
        (right, lower) : the lower right corner

        The coordinate has the y-axis going downwards
        """
        self.left = left
        self.upper = upper
        self.right = right
        self.lower = lower

    def width(self):
        return self.right - self.left

    def height(self):
        return self.lower - self.upper

    def center(self):
        return ((self.right + self.left) / 2, (self.lower + self.upper) / 2)


def crop(image: Image, product_finder: Callable[[Image], Rectangle]):
    product: Rectangle = product_finder(image)

    cropped = _calculate_crop_rectangle(product)

    return image.crop((cropped.left, cropped.upper, cropped.right, cropped.lower))


def _calculate_crop_rectangle(product: Rectangle) -> Rectangle:
    """Given the smallest rectangle containing the product, find the
    appropriate rectangle for cropping to, depending on the aspect
    ratio and padding.
    """
    width_cropped = max(product.width(), product.height() * ASPECT_RATIO) + WIDTH_PADDING
    height_cropped = width_cropped / ASPECT_RATIO
    cropped_center_row, cropped_center_column = product.center()

    left_cropped = cropped_center_column - width_cropped / 2
    upper_cropped = cropped_center_row - height_cropped / 2
    right_cropped = left_cropped + width_cropped
    lower_cropped = upper_cropped + height_cropped

    return Rectangle(left_cropped, upper_cropped, right_cropped, lower_cropped)
