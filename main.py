from PIL import Image
import os
from cropper import crop
from uniform_background import uniform_background_product_finder


def main(filename):
    with Image.open(filename) as img:

        # TODO: The same cropping function `crop` can be used with other
        # "product finders". Here uses just the product finder for a simple
        # uniform white background.
        cropped_image = crop(img, uniform_background_product_finder)

        cropped_image.show()

        return cropped_image

def multiple(inputdir, outputdir=None):
    if outputdir is not None:
        if not os.path.exists(outputdir): os.mkdir(outputdir)
        
    for filename in os.listdir(inputdir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image = main(inputdir + "/" + filename)
            if outputdir is not None:
                image.save(outputdir + "/" + filename)


if __name__ == '__main__':
    multiple("images/unedited_uniform_background")
