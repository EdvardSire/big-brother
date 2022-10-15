import torch
from json import dumps
import cv2
from upload import upload
from msg import send_message
from threading import Thread, local
from time import sleep
from tools import TOOLS_LIST


BOUNDING_COLOR = (0, 255, 0)
HEIGHT_OFFSET = 384
WIDTH_OFFSET = 640
ABOVE_BELOW_SPLIT = 515
NUMBER_OF_SAMPLES_BEFORE_UPLOAD = 20
SAMPLE_POLLING_TIME = 2
DETECTION_ACCURACY = 0.5


# def draw_boundingboxes(buffer, data):
#     xmax, ymax = data[3]
#     buffer = cv2.rectangle(buffer, data[2], data[3], BOUNDING_COLOR, 2)
#     buffer = cv2.putText(buffer, data[0], (xmax + 10, ymax), 0, 1, BOUNDING_COLOR, 2)

#     return buffer


def draw_boundingboxes(buffer, data, object):
    xymin, xymax = data
    buffer = cv2.rectangle(buffer, xymin, xymax, BOUNDING_COLOR, 2)
    buffer = cv2.putText(buffer, object, (xymax[0] + 10, xymax[1]), 0, 1, BOUNDING_COLOR, 2)
    
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


def detection_over_time(data_over_time):
    for tool in data_over_time:
        if data_over_time[tool][0] > NUMBER_OF_SAMPLES_BEFORE_UPLOAD // 2:
            return True, tool, (data_over_time[tool][1], data_over_time[tool][2])

    return False, None, None


def remove_unwanted_detections(data):
    sanitized_data = []
    for detection in data:
        if detection[0] in TOOLS_LIST:
            sanitized_data.append(detection)

    return sanitized_data


def initialize_dict():
    new_dict = dict()
    for tool in TOOLS_LIST:
        new_dict.update({tool: [0, (0, 0), (0, 0)]})
    
    print("CLEARED OUT DICT")
    return new_dict


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

    data_over_time = initialize_dict()
    LOOP_NUMBER = 0

    while True:
        data = []  # [(name, percent, (xmin, ymin), (xmax, ymax))]
        below_data = []
        above_data = []
        buffer = frame
        buffer_left = buffer[HEIGHT_OFFSET:, :WIDTH_OFFSET]
        buffer_right = buffer[HEIGHT_OFFSET:, WIDTH_OFFSET:]
        unique_detections = set()

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
        data = remove_unwanted_detections(data)
        # print("DATA", data)

        for value in data:
            if (value[2][1] + value[3][1]) // 2 > ABOVE_BELOW_SPLIT:
                below_data.append(value)
                unique_detections.add(value[0])
            else:
                above_data.append(value)
        # print("UNIQUE DETECTIONS", unique_detections)

        for tool in unique_detections:
            xymin, xymax = tuple(), tuple()
            for detection in below_data:
                if tool == detection[0]:
                    xymin = detection[2]
                    xymax = detection[3]

            data_over_time[tool][0] += 1
            if not len(xymin) == 0:
                data_over_time[tool][1] = xymin
                data_over_time[tool][2] = xymax

        print(data_over_time)

        # See the ABOVE_BELOW_SPLIT
        # buffer = cv2.rectangle(
        #     buffer, (0, ABOVE_BELOW_SPLIT), (1000, ABOVE_BELOW_SPLIT), (0, 255, 0), 2
        # )

        if LOOP_NUMBER == NUMBER_OF_SAMPLES_BEFORE_UPLOAD:
            to_upload, object, xyminmax = detection_over_time(data_over_time)
            if to_upload:
                draw_boundingboxes(buffer, xyminmax, object)
                cv2.imwrite("UPLOAD_IMG.jpg", buffer)
                upload("UPLOAD_IMG.jpg", object, log_state=False)
            else:
                message = "no detection"
                send_message("hardware_bad", message)
            data_over_time = initialize_dict()
            LOOP_NUMBER = 0
            print("DONE ONE LOOP")

        # upload("UPLOAD_IMG.jpg", data, log_state=False)
        # upload("runs/detect/exp/image1.jpg", data, log_state=False)

        print()
        sleep(SAMPLE_POLLING_TIME)
        LOOP_NUMBER += 1


if __name__ == "__main__":
    # model = torch.hub.load("ultralytics/yolov5", "yolov5s")
    model = torch.hub.load("ultralytics/yolov5", "custom", path="best.pt")
    stream = cv2.VideoCapture("rtsp://big-brother:8554/ueye")

    if not stream.isOpened():
        print("Cannot reach stream")
        exit()

    Thread(target=update_videofeed).start()
    sleep(1)  ## ABSOLUTELY NECESSARY
    Thread(target=use_image).start()
