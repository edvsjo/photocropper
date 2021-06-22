from PIL import Image

from cropper import crop
from uniform_background import uniform_background_product_finder


def main(filename):
    with Image.open(filename) as img:

        # TODO: The same cropping function `crop` can be used with other
        # "product finders". Here uses just the product finder for a simple
        # uniform white background.
        cropped_image = crop(img, uniform_background_product_finder)

        cropped_image.show()


if __name__ == '__main__':
    main("images/Adidas-Daily-3_484621_60_extra6_unedited.jpg")
