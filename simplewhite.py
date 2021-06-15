import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("images/Runfalcon_2.0_Sko_Svart_GZ7418_01_standard.jpg")

grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def most_common_color(image):
    values, counts = np.unique(grey, return_counts=True)
    color = values[np.argmax(counts)]
    return color


def find_bountries(image, color=255):
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

    objectHeight = abs(lastRow - firstRow)
    objectWidth =  abs(lastCol - firstCol)

    if objectHeight > objectWidth:
        cropHeight = objectHeight + 100
        cropWidth = cropHeight * (1500/1814)
    else:
        cropWidth = objectWidth + 100
        cropHeight = cropWidth * (1814/1500)
    
    objectCenterRow = (firstRow + lastRow)//2
    objectCenterCol = (firstCol + lastCol)//2

    fromRow = objectCenterRow - (cropHeight//2)
    toRow = objectCenterRow + (cropHeight//2)
    fromCol = objectCenterCol - (cropWidth//2)
    toCol = objectCenterCol + (cropWidth//2)
    
    print(fromRow, toRow, fromCol, toCol)
    cropped = image[fromRow:toRow, fromCol:toCol]
    return cropped



common_color = most_common_color(grey)
print(common_color)

firstRow, firstCol, lastRow, lastCol = find_bountries(grey, common_color)

print(firstRow, firstCol)
print(lastRow, lastCol)


grey[firstRow] = 0
grey[lastRow] = 0
grey[:, firstCol] = 0
grey[:, lastCol] = 0

cropped = crop_image(grey, firstRow, lastRow, firstCol, lastCol)

# cv2.imshow("testin", grey)
# cv2.waitKey(0)

plt.imshow(grey, 'gray')
plt.imshow(cropped, 'cropped')
plt.show()
