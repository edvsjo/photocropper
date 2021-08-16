from PIL import Image
import os
import sys
import fnmatch
from cropper import crop
from uniform_background import uniform_background_product_finder
from persondetect import person_detector

def main(filename, detector=0):
    with Image.open(filename) as img:
        # TODO: The same cropping function `crop` can be used with other
        # "product finders". Here uses just the product finder for a simple
        # uniform white background.

        # cropped = crop(img, uniform_background_product_finder)
        cropped = crop(img, PRODUCT_FINDERS[detector])
        resized = cropped.resize((1500, 1814), Image.BICUBIC)
        # resized.save("images/temp.jpg")
        resized.show()
        return resized


def multiple(inputdir, outputdir=None, detector=0):
    if outputdir is not None:
        if not os.path.exists(outputdir): os.mkdir(outputdir)
    
    accepted_file_types = ('*.jpg', '*.jpeg', '*.gif', '*.png')
    total=0
    for root, dirs, files in os.walk(inputdir):
        for extension in accepted_file_types:
            for filename in fnmatch.filter(files, extension):
                total+=1

    count = 0
    for root, dirs, files in os.walk(inputdir):
        for extension in accepted_file_types:
            for filename in fnmatch.filter(files, extension):
                count += 1
                print(str(count) + "/" + str(total))
                img = Image.open(inputdir + "/" + filename)
                cropped = crop(img, PRODUCT_FINDERS[detector])
                resized = cropped.resize((1500, 1814), Image.BICUBIC)
                if outputdir is not None:
                    icc = img.info.get('icc_profile')
                    resized.save(outputdir + "/" + filename, "JPEG", icc_profile=icc)
                    print(filename)


if __name__ == '__main__':
    PRODUCT_FINDERS = [uniform_background_product_finder, person_detector]
    if len(sys.argv) == 1:
        multiple("/Users/sportmannimac/Downloads/input", "/Users/sportmannimac/Downloads/output")
        # main('/Users/sportmannimac/Documents/Bilder/Adidas/Uredigert/Adidas-Anorakk-Dame_483897_41_extra5.jpg')
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) == 3:
        multiple(sys.argv[1], sys.argv[2])
    else:
        multiple(sys.argv[1], sys.argv[2], int(sys.argv[3]))


