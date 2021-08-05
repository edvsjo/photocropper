import torch
from PIL import Image
from cropper import Rectangle

def person_detector(image: Image) -> Rectangle:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    result = model(image)
    left = int(result.pandas().xyxy[0].xmin)
    right = int(result.pandas().xyxy[0].xmax)
    top = int(result.pandas().xyxy[0].ymin)
    bot = int(result.pandas().xyxy[0].ymax)
    return Rectangle(left, top, right, bot)
