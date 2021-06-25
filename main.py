from PIL import Image

from cropper import crop, draw_crop_rectangle
from uniform_background import uniform_background_product_finder


def main(filename):
    with Image.open(filename) as img:
        # TODO: The same cropping function `crop` can be used with other
        # "product finders". Here uses just the product finder for a simple
        # uniform white background.
        drawn_crop_rectangle = draw_crop_rectangle(img, uniform_background_product_finder)
        drawn_crop_rectangle.show()


if __name__ == '__main__':
    main("images/unedited_uniform_background/Adidas-Advantage-Sneakers_484619_10_extra1.jpg")
