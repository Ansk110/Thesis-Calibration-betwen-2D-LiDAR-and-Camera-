import cv2
import numpy as np

image = cv2.imread('/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Images/img_5.jpg') 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()
corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

if corners:
    img_points = np.concatenate(corners).squeeze()
    print("Image Points:\n", img_points)
    image_with_markers = cv2.aruco.drawDetectedMarkers(image.copy(), corners, ids)
    cv2.imshow('Detected Markers', image_with_markers)
    cv2.waitKey(0)
else:
    print("No ArUco markers detected in the image.")
