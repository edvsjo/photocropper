import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("images/Adidas-VL-court-2_484630_60_extra7-kopi.jpg")

grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def most_common_color(image):
    values, counts = np.unique(grey, return_counts=True)
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
    cropHeight = 0
    cropWidth = 0
    objectWidth = abs(firstCol - lastCol)
    objectHeight = abs(firstRow - lastRow)
    scalePercent = 0
    if objectWidth >= objectHeight:
        cropWidth = objectWidth + objectWidth*0.1
        scalePercent = 1500 / (objectWidth +objectWidth*0.07)
    else:
        cropHeight = objectHeight + objectHeight*0.1
        scalePercent = 1814 / (objectHeight + objectHeight*0.07)
    
    width = int(image.shape[1] * scalePercent)
    height = int(image.shape[0] * scalePercent)
    resized = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    greyResized = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    rFirstRow, rFirstCol, rLastRow, rLastCol = find_boundries(greyResized, 237)
    # image[firstRow] = 0
    # image[lastRow] = 0
    # image[:, firstCol] = 0
    # image[:, lastCol] = 0
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

    objectCenterRow = int((rFirstRow + rLastRow)/2)
    objectCenterCol = int((rFirstCol + rLastCol)/2)

    fromCol = objectCenterCol - 750
    toCol = objectCenterCol + 750
    fromRow = objectCenterRow - 907
    toRow = objectCenterRow + 907

    cropped = resized[fromRow:toRow, fromCol:toCol]
    return cropped



common_color = most_common_color(grey)
print(common_color)

firstRow, firstCol, lastRow, lastCol = find_boundries(grey, common_color)


cropped = crop_image(img, firstRow, lastRow, firstCol, lastCol)
print(cropped.shape)
cv2.imshow("cropped", cropped)
cv2.waitKey(0)

plt.imshow(grey, 'gray')
plt.imshow(cropped, 'cropped')
plt.show()
