import torch
import cv2
import os


model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

stream = cv2.VideoCapture("rtsp://big-brother:8554/ueye")


if not stream.isOpened():
    print("Cannot reach stream")
    exit()

ret, frame = stream.read()
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

if not ret:
    print("Can't recieve image")
    exit()

model(frame).save()
os.system("python3 upload.py runs/detect/exp/image0.jpg")
