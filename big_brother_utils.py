import cv2
from numpy import ndarray
from typing import Tuple

# Local
from constants import *


def draw_boundingboxes(buffer: ndarray, data: tuple, object: str) -> ndarray:
    xymin, xymax = data
    buffer = cv2.rectangle(buffer, xymin, xymax, BOUNDING_COLOR, 2)
    buffer = cv2.putText(
        buffer, object, (xymax[0] + 10, xymax[1]), 0, 1, BOUNDING_COLOR, 2
    )

    return buffer


def format_left_data(
    name: str, percentage: float, xymin: tuple, xymax: tuple
) -> Tuple[str, float, Tuple[int, int], Tuple[int, int]]:
    xmin, ymin = xymin
    xmax, ymax = xymax
    ymin += HEIGHT_OFFSET
    ymax += HEIGHT_OFFSET

    return (name, percentage, (int(xmin), int(ymin)), (int(xmax), int(ymax)))


def format_right_data(
    name: str, percentage: float, xymin: tuple, xymax: tuple
) -> Tuple[str, float, Tuple[int, int], Tuple[int, int]]:
    xmin, ymin = xymin
    xmax, ymax = xymax
    ymin += HEIGHT_OFFSET
    ymax += HEIGHT_OFFSET
    xmin += WIDTH_OFFSET
    xmax += WIDTH_OFFSET

    return (name, percentage, (int(xmin), int(ymin)), (int(xmax), int(ymax)))


def detection_over_time(data_over_time) -> tuple[bool, str, tuple]:
    for tool in data_over_time:
        if data_over_time[tool][0] > NUMBER_OF_SAMPLES_BEFORE_UPLOAD // 2:
            return True, tool, (data_over_time[tool][1], data_over_time[tool][2])

    return False, str(), tuple()


def remove_unwanted_detections(data: list) -> list:
    sanitized_data = []
    for detection in data:
        if detection[0] in TOOLS_LIST:
            sanitized_data.append(detection)

    return sanitized_data


def initialize_dict() -> dict:
    new_dict = dict()
    for tool in TOOLS_LIST:
        new_dict.update({tool: [0, (0, 0), (0, 0)]})

    print("CLEARED OUT DICT")
    return new_dict
