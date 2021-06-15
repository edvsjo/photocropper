import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("images/Kaffe-Naya-Kjole-spm_354208_70_extra7.jpg")

grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

boxes, weights = hog.detectMultiScale(grey, winStride=(8, 8))
for (xA, yA, xB, yB) in boxes:
    cv2.rectangle(grey, (xA, yA), (xB, yB), (0, 255, 0), 2)

plt.imshow(grey, 'gray')
plt.show()
