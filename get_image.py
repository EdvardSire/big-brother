import torch
import cv2
from upload import upload
from threading import Thread
from time import sleep


BOUNDING_COLOR = (0, 255, 0)
HEIGHT_OFFSET = 384
WIDTH_OFFSET = 640
ABOVE_BELOW_SPLIT = 620


# model = torch.hub.load("ultralytics/yolov5", "yolov5s")
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
stream = cv2.VideoCapture("rtsp://big-brother:8554/ueye")

if not stream.isOpened():
    print("Cannot reach stream")
    exit()


def draw_boundingboxes(buffer, data):
    xmax, ymax = data[3]
    buffer = cv2.rectangle(buffer, data[2], data[3], BOUNDING_COLOR, 2)
    buffer = cv2.putText(buffer, data[0], (xmax + 10, ymax), 0, 1, BOUNDING_COLOR, 2)

    return buffer


def format_left_data(name, percentage, xymin, xymax):
    xmin, ymin = xymin
    xmax, ymax = xymax
    ymin += HEIGHT_OFFSET
    ymax += HEIGHT_OFFSET

    return (name, percentage, (int(xmin), int(ymin)), (int(xmax), int(ymax)))


def format_right_data(name, percentage, xymin, xymax):
    xmin, ymin = xymin
    xmax, ymax = xymax
    ymin += HEIGHT_OFFSET
    ymax += HEIGHT_OFFSET
    xmin += WIDTH_OFFSET
    xmax += WIDTH_OFFSET

    return (name, percentage, (int(xmin), int(ymin)), (int(xmax), int(ymax)))


def update_videofeed():
    print("VIDEOFEED STARTUP")
    global frame

    while True:
        did_read, frame = stream.read()
        frame = cv2.flip(frame, -1)
        if not did_read:
            print("Can't recieve image")


def use_image():
    print("MODEL STARTUP")

    while True:
        data = []  # [(name, percent, (xmin, ymin), (xmax, ymax))]
        buffer = frame
        buffer_left = buffer[HEIGHT_OFFSET:, :WIDTH_OFFSET]
        buffer_right = buffer[HEIGHT_OFFSET:, WIDTH_OFFSET:]

        result = model([buffer_left, buffer_right])
        print(result.pandas().xyxy[0])
        print(result.pandas().xyxy[1])

        # get data for right image
        for i in range(len(result.pandas().xyxy[0])):
            foo = result.pandas().xyxy[0]
            data.append(
                format_left_data(
                    foo["name"][i],
                    foo["confidence"][i],
                    (foo["xmin"][i], foo["ymin"][i]),
                    (foo["xmax"][i], foo["ymax"][i]),
                )
            )
        # get data for left image
        for i in range(len(result.pandas().xyxy[1])):
            foo = result.pandas().xyxy[1]
            data.append(
                format_right_data(
                    foo["name"][i],
                    foo["confidence"][i],
                    (foo["xmin"][i], foo["ymin"][i]),
                    (foo["xmax"][i], foo["ymax"][i]),
                )
            )
        print(data)

        # See the ABOVE_BELOW_SPLIT
        # buffer = cv2.rectangle(buffer, (0, above_below_split), (1000, above_below_split), (0, 255, 0), 2)

        below_data = []
        above_data = []
        for value in data:
            if (value[2][1] + value[3][1]) // 2 > ABOVE_BELOW_SPLIT:
                below_data.append(value)
            else:
                above_data.append(value)

        print("Above data:", above_data)
        print("Below data:", below_data)

        for bounding_box_data in range(len(data)):
            buffer = draw_boundingboxes(buffer, data[bounding_box_data])


        cv2.imwrite("UPLOAD_IMG.jpg", buffer)
        upload("UPLOAD_IMG.jpg", data, log_state=False)
        # upload("runs/detect/exp/image1.jpg", data, log_state=False)

        print("DONE DELETING")
        print()
        sleep(8)


Thread(target=update_videofeed).start()
sleep(1)  ## ABSOLUTELY NECESSARY
Thread(target=use_image).start()

