from typing import Callable, Tuple
from operator import sub
from PIL import Image, ImageDraw
import cv2
import numpy as np

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

    def draw(self, image: Image):
        """Draw the rectangle on a image"""
        draw = ImageDraw.Draw(image)
        draw.line([
            (self.left, self.upper),
            (self.right, self.upper),
            (self.right, self.lower),
            (self.left, self.lower),
            (self.left, self.upper)
        ], width=3, fill=(0, 0, 0))

        return image

    def encloses(self, other_rectangle) -> bool:
        """ Fully encloses the other rectangle """
        return (
            self.left < other_rectangle.left and
            self.right > other_rectangle.right and
            self.upper < other_rectangle.upper and
            self.lower > other_rectangle.lower)

    def pad_to_fill(self, image: Image):
        """Pad the image until it fills the rectangle. Position of the
        original image will be relative to the rectangle: if the (left,
        upper) of the rectangle is (-10, -15) the original image will
        start at (10, 15) in the new image. The latter means the rectangle
        will also act as a crop-rectangle, if the old image overflows to
        its outsides.
        """
        dominant_color = self.dominant_color_in_rect(image)
        # new_image = Image.new(image.mode, (int(self.width()), int(self.height())), dominant_color)
        new_image = Image.new(image.mode, (int(self.width()), int(self.height())), (0, 255, 0))
        new_image.paste(image, (- int(self.left), - int(self.upper)))
        mask = self.draw_mask(new_image)

        #Convert the image to cv format and perform the inpainting
        cv_image = cv2.cvtColor(np.array(new_image), cv2.COLOR_RGB2BGR)
        edited = cv2.inpaint(cv_image, mask, 5, cv2.INPAINT_TELEA)

        #Convert back to PIL format
        PIL_edited = Image.fromarray(cv2.cvtColor(np.array(edited), cv2.COLOR_BGR2RGB))
        return PIL_edited

    def draw_mask(self, image: Image):
        """Create a mask of what the pad_to_fill function filled in"""
        np_image = np.array(image)
        mask = (np_image[:, :, 0]==0) & (np_image[:, :, 1]==255) & (np_image[:, :, 2]==0)
        mask_image = (mask*255).astype(np.uint8)
        return mask_image


    def move_to_align_with_corner(self, align_with, corner: Tuple[int, int]):
        """ Corners: (-1, -1) = left upper, (-1, 1) = left lower,
        (1, -1) = right upper, (1, 1) = right lower. A value of
        0 means do not align in this direction; e.g. (-1, 0) is align
        left without changing the location in the y-direction.
        Keeps the width and height of the original rectangle. """
        right = corner[0] == 1
        left = corner[0] == -1
        lower = corner[1] == 1
        upper = corner[1] == -1

        width = self.width()
        height = self.height()

        if right:
            self.right = align_with.right
            self.left = self.right - width
        elif left:
            self.left = align_with.left
            self.right = self.left + width

        if lower:
            self.lower = align_with.lower
            self.upper = self.lower - height
        elif upper:
            self.upper = align_with.upper
            self.lower = self.upper + height

        return self

    def dominant_color_in_rect(self, img: Image):
        colors = img.getcolors(int(self.width() * self.height()))
        sorted_colors = sorted(colors, key=lambda x: x[0])
        dominant_color = sorted_colors[-1][1]
        return dominant_color

    def __str__(self):
        return f"{self.left} {self.upper} {self.right} {self.lower}"

    @staticmethod
    def border(image: Image):
        return Rectangle(0, 0, *image.size)


def crop(image: Image, product_finder: Callable[[Image], Rectangle]):
    product: Rectangle = product_finder(image)
    image_border = Rectangle.border(image)
    cropped = _calculate_crop_rectangle(product, image_border)
    return cropped.pad_to_fill(image)


def _calculate_crop_rectangle(product: Rectangle, image_border: Rectangle) -> Rectangle:
    """Given the smallest rectangle containing the product, find the
    appropriate rectangle for cropping to, depending on the aspect
    ratio and padding.
    """
    width_cropped = max(product.width(), product.height() * ASPECT_RATIO) + WIDTH_PADDING
    height_cropped = width_cropped / ASPECT_RATIO
    cropped_center_column, cropped_center_row = product.center()

    left_cropped = cropped_center_column - width_cropped / 2
    upper_cropped = cropped_center_row - height_cropped / 2
    right_cropped = left_cropped + width_cropped
    lower_cropped = upper_cropped + height_cropped

    crop_rectangle = Rectangle(left_cropped, upper_cropped, right_cropped, lower_cropped)

    if image_border.encloses(crop_rectangle):
        return crop_rectangle

    # When the crop rectangle goes outside the image, it is usually because
    # the product is located at the edge of the image. Keep the aspect ratio,
    # but move the crop rectangle so that its edges are aligned with the edges
    # where the product goes outside the image.
    product_corner = _alignement_corner_for_crop_overflow_fix(product, crop_rectangle, image_border)

    return crop_rectangle.move_to_align_with_corner(product, product_corner)


def _alignement_corner_for_crop_overflow_fix(product, crop_rectangle, image_border):
    product_corner = _corner_with_product(product, image_border)

    if not _left_right_align_edge(product, crop_rectangle, image_border):
        product_corner = (0, product_corner[1])
    if not _upper_lower_align_edge(product, crop_rectangle, image_border):
        product_corner = (product_corner[0], 0)

    return product_corner


def _left_right_align_edge(product, crop_rectangle, image_border):
    """ Should we align the left/right edge of the crop with the left/right
    edge of the product? """
    width_overflows = (crop_rectangle.left < image_border.left or
                       crop_rectangle.right > image_border.right)

    product_at_left_right_border = (product.left <= image_border.left or
                                    product.right >= image_border.right)

    return width_overflows and product_at_left_right_border


def _upper_lower_align_edge(product, crop_rectangle, image_border):
    """ Should we align the upper/lower edge of the crop with the upper/lower
    edge of the product? """
    height_overflows = (crop_rectangle.upper < image_border.upper or
                        crop_rectangle.lower > image_border.lower)

    product_at_upper_lower_border = (product.upper <= image_border.upper or
                                     product.lower >= image_border.lower)

    return height_overflows and product_at_upper_lower_border


def _corner_with_product(product: Rectangle, image_border: Rectangle) -> Tuple[int, int]:
    """ Corners: (-1, -1) = left upper, (-1, 1) = left lower,
    (1, -1) = right upper, (1, 1) = right lower. A value of
    0 means the product is centered in this direction. """
    delta_x_product, delta_y_product = _tuple_subtract(product.center(),
                                                       image_border.center())
    return (_sign(delta_x_product), _sign(delta_y_product))


def _tuple_subtract(tuple_1, tuple_2):
    return tuple(map(sub, tuple_1, tuple_2))


def _sign(x) -> int:
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0
