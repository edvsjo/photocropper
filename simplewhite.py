import cv2
import numpy as np
import imutils
from PIL import Image, ImageOps
from matplotlib import pyplot as plt

# img = cv2.imread("images/Adidas-VL-court-2_484630_60_extra3.jpg")
img = Image.open("images/Adidas-Daily-3_484621_60_extra6_unedited.jpg")

# grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def most_common_color(image):
    values, counts = np.unique(image, return_counts=True)
    color = values[np.argmax(counts)]
    return color


def find_boundries(image, color=255):
    firstRow = 100000000
    firstCol = 100000000
    lastRow = -1
    lastCol = -1
    for row in range(len(image)):
        for pixelIndex in range(len(image[row])):
            if firstRow>row and image[row][pixelIndex] != color:
                firstRow = row
            if lastRow < row and image[row][pixelIndex] != color:
                lastRow = row
            if firstCol > pixelIndex and image[row][pixelIndex] != color:
                firstCol = pixelIndex
            if lastCol < pixelIndex and image[row][pixelIndex] != color:
                lastCol = pixelIndex
    return firstRow, firstCol, lastRow, lastCol


def crop_image(image, firstRow, lastRow, firstCol, lastCol):
    objectWidth = abs(firstCol - lastCol)
    objectHeight = abs(firstRow - lastRow)
    scalePercent = 0

    if objectWidth >= objectHeight:
        cropWidth = objectWidth + objectWidth*0.1
        scalePercent = 1500 / (objectWidth +objectWidth*0.07)
    else:
        cropHeight = objectHeight + objectHeight*0.1
        scalePercent = 1814 / (objectHeight + objectHeight*0.07)
    
    width = max(1500, int(image.shape[1] * scalePercent))
    height = max(1814, int(image.shape[0] * scalePercent))
    resized = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

    greyResized = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    rFirstRow, rFirstCol, rLastRow, rLastCol = find_boundries(greyResized, 237)

    objectCenterRow = int((rFirstRow + rLastRow)/2)
    objectCenterCol = int((rFirstCol + rLastCol)/2)

    fromCol = objectCenterCol - 750
    toCol = objectCenterCol + 750
    fromRow = objectCenterRow - 907
    toRow = objectCenterRow + 907

    print(fromRow, toRow)
    print(fromCol, toCol)
    print(resized.shape)

    cropped = resized[fromRow:toRow, fromCol:toCol]
    return cropped


# common_color = most_common_color(grey)
# print(common_color)

# firstRow, firstCol, lastRow, lastCol = find_boundries(grey, common_color)

# img[firstRow] = 0
# img[lastRow] = 0
# img[:, firstCol] = 0
# img[:, lastCol] = 0
# resized[rFirstRow] = 0
# resized[rLastRow] = 0
# resized[:, rFirstCol] = 0
# resized[:, rLastCol] = 0

# print(abs(firstRow- lastRow))
# print(abs(firstCol- lastCol))
# print(abs(rFirstRow- rLastRow))
# print(abs(rFirstCol- rLastCol))
# cv2.imshow("original", image)
# cv2.imshow("resized", resized)
# cv2.waitKey(0)


# cropped = crop_image(img, firstRow, lastRow, firstCol, lastCol)
# print(cropped.shape)
# cv2.imshow("cropped", cropped)
# cv2.waitKey(0)

# plt.imshow(grey, 'gray')
# plt.imshow(cropped, 'cropped')
# plt.show()

img.load()

inverted = ImageOps.invert(img)

image_data = np.array(inverted)

color = most_common_color(image_data)
print(color)

image_data_bw = image_data.max(axis=2)
non_empty_cols = np.where(image_data_bw.max(axis=0)>0)[0]
non_empty_rows = np.where(image_data_bw.max(axis=1)>0)[0]
cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_cols), max(non_empty_cols))

image_data_new = image_data[cropBox[0]:cropBox[1]+1, cropBox[2]:cropBox[3]+1 , :]

print(image_data_new[0][0])

cropped = Image.fromarray(image_data_new)
cropped.show()
cropped.save("testing_cropped.png")

# inversed = ImageOps.invert(img)
# imageBox = inversed.getbbox()
# cropped = img.crop(imageBox)
# img.show()


