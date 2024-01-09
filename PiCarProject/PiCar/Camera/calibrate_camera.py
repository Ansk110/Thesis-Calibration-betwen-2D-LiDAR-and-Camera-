import cv2
import numpy as np
import glob

# Define ArUco dictionary and parameters
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)  # Change the dictionary type if needed
parameters = cv2.aruco.DetectorParameters_create()

# Arrays to store object points and image points from all images
obj_points = []  # 3D points in real-world space
img_points = []  # 2D points in image plane

# Find calibration images
calibration_images = glob.glob('/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Images/img_5.jpg')

for fname in calibration_images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect ArUco markers
    corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if corners:
        # Draw and display the detected markers
        img = cv2.aruco.drawDetectedMarkers(img, corners, ids)
        cv2.imshow('img', img)
        # Display the image until 'q' is pressed
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
       
        # Define the object points for the ArUco marker (assuming a square marker of side length 0.04 units)
        objp = np.array([[0, 0, 0], [0.04, 0, 0], [0.04, 0.04, 0], [0, 0.04, 0]], dtype=np.float32)
        obj_points.append(objp)

        img_points.append(corners[0])  # Assuming only one marker is detected per image

cv2.destroyAllWindows()

# Perform camera calibration
ret, camera_matrix, dist_coeffs, _, _ = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

# Save the obtained calibration parameters
np.savez('intrinsic_params_1.npz', camera_matrix=camera_matrix, dist_coeffs=dist_coeffs)
