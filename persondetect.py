import torch
from PIL import Image

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
image1 = Image.open('/Users/sportmannimac/Documents/photocropper/images/unedited_noisy_background/Hummel-Leagacy-Tapered-Pants_483983_40_extra1.jpg')
# image2 = Image.open('/Users/sportmannimac/Documents/photocropper/images/unedited_noisy_background/Hummel-Leagacy-Tapered-Pants_483983_40_extra2.jpg')
# image3 = Image.open('/Users/sportmannimac/Documents/photocropper/images/unedited_noisy_background/Hummel-Leagacy-Tapered-Pants_483983_40_extra3.jpg')

results = model([image1])

results.show()
print(results.pandas().xyxy[0])
