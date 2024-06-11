import cv2 as cv
import os
import numpy as np

aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
marker_id = 0
marker_size_mm = 73

objp = np.array([[0, 0, 0], [marker_size_mm, 0, 0], [marker_size_mm, marker_size_mm, 0], [0, marker_size_mm, 0]], dtype=np.float32)


obj_points_3D = []
img_points_2D = []

image_path = "/PiCarProject/PiCar/Camera/Images/img_1.jpg"

image = cv.imread(image_path)
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

corners, ids, _ = cv.aruco.detectMarkers(gray, aruco_dict)

if ids is not None and marker_id in ids:
    marker_index = np.where(ids == marker_id)[0][0]
    marker_corners = corners[marker_index][0]

    obj_points_3D.append(objp)
    img_points_2D.append(marker_corners)

    cv.aruco.drawDetectedMarkers(image, corners)
    cv.imshow('Detected ArUco Marker', image)
    cv.waitKey(1000)

cv.waitKey()
cv.destroyAllWindows()

