import torch
from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB
from shutil import rmtree
from upload import upload


model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

stream = VideoCapture("rtsp://big-brother:8554/ueye")


if not stream.isOpened():
    print("Cannot reach stream")
    exit()


# ret = 1 if the image can be retrieved
ret, frame = stream.read()
frame = cvtColor(frame, COLOR_BGR2RGB)


if not ret:
    print("Can't recieve image")
    exit()


# Run the model
result = model(frame)
# YOLOv5 evaluates the image and save it to runs/detect/exp/image0.jpg
result.save()


# Where xyxy[i] is the i'th image
print(result.pandas().xyxy[0])
# print(result.pandas().xyxy[0]['name'])
detections = result.pandas().xyxy[0]['name']
confidence = result.pandas().xyxy[0]['confidence']


detection_pairs = []
for i in range(detections.size):
    detection_pairs.append((detections.loc[i], confidence.loc[i]))

print(detection_pairs)

# Uploads the image to Slack
upload("runs/detect/exp/image0.jpg", detection_pairs)
rmtree("./runs")
