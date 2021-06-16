import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("images/Twentyfour-Isbre-Ecodown-Jakke_484612_30_extra4.Jpeg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.1, 4)

for (xA, yA, xB, yB) in faces:
    cv2.rectangle(gray, (xA, yA), (xB, yB), (0, 255, 0), 2)

# boxes, weights = hog.detectMultiScale(grey, winStride=(8, 8))
# hog = cv2.HOGDescriptor()
# hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


plt.imshow(gray, 'gray')
plt.show()
