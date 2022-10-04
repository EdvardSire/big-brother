import torch
from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB
from os import system
from shutil import rmtree


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


# YOLOv5 evaluates the image and save it to runs/detect/exp/image0.jpg
model(frame).save()

# Uploads the image to Slack
system("python3 upload.py runs/detect/exp/image0.jpg")
rmtree("./runs")
