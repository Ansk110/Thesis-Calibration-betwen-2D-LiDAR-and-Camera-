import cv2
import numpy as np


def get_aruco_marker_corners(image):
    marker_id = 0
    margin_mm = 15
    margin_rect = margin_mm * np.array([
        [-1, -1],
        [1, -1],
        [1, 1],
        [-1, 1],
    ])

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters_create()
    corners, ids, _ = cv2.aruco.detectMarkers(gray, dictionary, parameters=parameters)
    if ids is not None and marker_id in ids:
        marker_index = np.where(ids == marker_id)[0][0]
        marker_corners = corners[marker_index][0].astype(int)
        outer_corners = marker_corners + margin_rect
        return outer_corners
    return []


def get_aruco_marker_inner_corners(image):
    marker_id = 0
    margin_mm = 15
    margin_rect = margin_mm * np.array([
        [-1, -1],
        [1, -1],
        [1, 1],
        [-1, 1],
    ])

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters_create()
    corners, ids, _ = cv2.aruco.detectMarkers(gray, dictionary, parameters=parameters)
    if ids is not None and marker_id in ids:
        marker_index = np.where(ids == marker_id)[0][0]
        marker_corners = corners[marker_index][0].astype(int)
        return marker_corners
    return []


def draw_aruco_markers(image, outer_corners):
    for i in range(4):
        point_a = tuple(outer_corners[i])
        point_b = tuple(outer_corners[(i+1) % 4])
        cv2.line(image, point_a, point_b, (0, 255, 0), 2)
