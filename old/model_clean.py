import torch
import cv2
from threading import Timer


model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

stream = cv2.VideoCapture("rtsp://big-brother:8554/ueye")

def loop():
    Timer(3.0, loop).start()

    if not stream.isOpened():
        print("Cannot reach stream")
        exit()

    ret, frame = stream.read()
    if not ret:
        print("Can't recieve image")
        exit()
    
    cv2.imshow("swag",
        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    )
    cv2.waitKey(0)
    
    

loop()