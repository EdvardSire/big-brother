import torch
import cv2 as cv
from PIL import Image



model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
turtle_string = 'img.jpg'
turtle_PIL = Image.open('img.jpg')
turtle_read = cv.imread('img.jpg')

turtle_read = cv.cvtColor(turtle_read, cv.COLOR_BGR2RGB)

l = [turtle_read, turtle_string]

stream = cv.VideoCapture("rtsp://big-brother:8554/ueye")

if not stream.isOpened():
    print("Cannot reach stream")
    exit()

ret, frame = stream.read()
frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

if not ret:
    print("Can't recieve frame")
    exit()


print(type(frame))
print(type(turtle_read))


res = model(frame)
res.print()
res.save()
print()
print(res)
print()
print(type(res))

cv.imshow("swag", turtle_read)
cv.waitKey(0)
cv.destroyAllWindows()
