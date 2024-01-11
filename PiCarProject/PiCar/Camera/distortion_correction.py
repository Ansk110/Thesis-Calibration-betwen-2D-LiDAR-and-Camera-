import cv2
import numpy as np

# Load the calibration parameters obtained from the previous calibration step
calibration_data = np.load('average_intrinsic_extrinsic_values.npz')
camera_matrix = calibration_data['avg_camera_matrix']
dist_coeffs = calibration_data['avg_dist_coeffs']

# Read a sample image for distortion correction
sample_img = cv2.imread('/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Images/img_1.jpg')

h, w = sample_img.shape[:2]

# Undistort the image using the obtained parameters
new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
undistorted_img = cv2.undistort(sample_img, camera_matrix, dist_coeffs, None, new_camera_matrix)

# Display the original and undistorted images
cv2.imshow('Original Image', sample_img)
cv2.imshow('Undistorted Image', undistorted_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the undistorted image
undistorted_image_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/undistorted_img.jpg'
cv2.imwrite(undistorted_image_path, undistorted_img)

print(f"The undistorted image is saved at: {undistorted_image_path}")
