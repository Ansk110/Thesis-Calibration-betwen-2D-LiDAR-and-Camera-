import cv2 as cv
import os
import numpy as np

# ArUco marker parameters
aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)  # Select ArUco dictionary
marker_id = 0  # Marker ID to detect
marker_size_mm = 100  # Marker size in millimeters

# Prepare object points for the ArUco marker
objp = np.array([[0, 0, 0], [marker_size_mm, 0, 0], [marker_size_mm, marker_size_mm, 0], [0, marker_size_mm, 0]], dtype=np.float32)

# Arrays to store object points and image points
obj_points_3D = []  # 3D points in real-world space
img_points_2D = []  # 2D points in image plane

image_path = "/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Images/img_1.jpg"  # Path to the image with an ArUco marker

image = cv.imread(image_path)
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

# Detect ArUco markers
corners, ids, _ = cv.aruco.detectMarkers(gray, aruco_dict)

# Check for the desired marker ID
if ids is not None and marker_id in ids:
    marker_index = np.where(ids == marker_id)[0][0]  # Find the index of the desired marker

    # Get corners of the marker with the selected ID
    marker_corners = corners[marker_index][0]

    # Append the object points (same for all markers) and image points
    obj_points_3D.append(objp)
    img_points_2D.append(marker_corners)

    # Draw and display the detected marker
    cv.aruco.drawDetectedMarkers(image, corners)
    cv.imshow('Detected ArUco Marker', image)
    cv.waitKey(1000)

cv.destroyAllWindows()

# Camera calibration
ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv.calibrateCamera(obj_points_3D, img_points_2D, gray.shape[::-1], None, None)

# Save the calibration data using numpy savez
calib_data_path = "/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera"  # Replace this with your desired path
np.savez(f"{calib_data_path}/ArUcoCalibrationData",
         camera_matrix=camera_matrix,
         dist_coeffs=dist_coeffs,
         rvecs=rvecs,
         tvecs=tvecs)

print("Calibration completed and data saved.")
