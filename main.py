from PIL import Image
import os
import sys
from cropper import crop
from uniform_background import uniform_background_product_finder


def main(filename):
    with Image.open(filename) as img:
        # TODO: The same cropping function `crop` can be used with other
        # "product finders". Here uses just the product finder for a simple
        # uniform white background.
        cropped = crop(img, uniform_background_product_finder)
        print(cropped.size)
        resized = cropped.resize((1500, 1814), Image.BICUBIC)
        # resized.save("images/temp.jpg")
        resized.show()
        return resized


def multiple(inputdir, outputdir=None):
    if outputdir is not None:
        if not os.path.exists(outputdir): os.mkdir(outputdir)

    for filename in os.listdir(inputdir):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".tif"):
            img = Image.open(inputdir + "/" + filename)
            cropped = crop(img, uniform_background_product_finder)
            resized = cropped.resize((1500, 1814), Image.BICUBIC)
            if outputdir is not None:
                resized.save(outputdir + "/" + filename)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        multiple("/Users/sportmannimac/Downloads", "/Users/sportmannimac/Downloads/output")
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        multiple(sys.argv[1], sys.argv[2])

