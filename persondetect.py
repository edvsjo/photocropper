from pandas.core.frame import DataFrame
import torch
from PIL import Image
from cropper import Rectangle
import pandas as pd

#Often cuts off shoes or hair
VERTICAL_PADDING = 15

def person_detector(image: Image) -> Rectangle:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    result = model(image)
    # result.show()
    detected_objects = result.pandas().xyxy[0]
    detected_people = detected_objects.loc[detected_objects["class"] == 0]

    left = int(detected_people.xmin)
    upper = int(detected_people.ymin)

    right = int(detected_people.xmax)
    lower = int(detected_people.ymax)
    return Rectangle(left, upper, right, lower)
