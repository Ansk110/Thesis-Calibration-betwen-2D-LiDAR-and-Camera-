import cv2
import numpy as np

# Load the calibration parameters obtained from the previous calibration step
calibration_data = np.load('intrinsic_params_1.npz')
camera_matrix = calibration_data['camera_matrix']
dist_coeffs = calibration_data['dist_coeffs']

# Read a sample image for distortion correction
sample_img = cv2.imread('/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Images/*.jpg')

h, w = sample_img.shape[:2]

# Undistort the image using the obtained parameters
new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
undistorted_img = cv2.undistort(sample_img, camera_matrix, dist_coeffs, None, new_camera_matrix)

# Display the original and undistorted images
cv2.imshow('Original Image', sample_img)
cv2.imshow('Undistorted Image', undistorted_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
