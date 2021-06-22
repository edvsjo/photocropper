import cv2
import numpy as np
import imutils
from matplotlib import pyplot as plt

img = cv2.imread("images/Twentyfour-Mellow-T-skjorte_484396_41_extra7.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def test_face_detector(img):
    face_cascade = cv2.CascadeClassifier("haarcascadeface.xml")
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    faces = face_cascade.detectMultiScale(img, 1.1, 4)

    for (xA, yA, xB, yB) in faces:
        cv2.rectangle(img, (xA, yA), (xB, yB), (0, 255, 0), 2)

    return img


def test_pedestrian_detector(img):
    img = imutils.resize(img, width=min(400, gray.shape[0]))

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    boxes, weights = hog.detectMultiScale(img, winStride=(4, 4), padding=(4, 4), scale=1.05)
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    for (x, y, w, h) in boxes:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    return img

faceimage = test_face_detector(gray)

cv2.imshow("facedetected", faceimage)
cv2.waitKey(0)
