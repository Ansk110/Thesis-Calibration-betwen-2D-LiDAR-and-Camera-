import cv2
import numpy as np

calibration_data = np.load('/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Intrinsic/intrinsic_params_1.npz')
camera_matrix = calibration_data['camera_matrix']
dist_coeffs = calibration_data['dist_coeffs']

sample_img = cv2.imread('/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Images/img_1.jpg')

h, w = sample_img.shape[:2]

new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
undistorted_img = cv2.undistort(sample_img, camera_matrix, dist_coeffs, None, new_camera_matrix)

cv2.imshow('Original Image', sample_img)
cv2.imshow('Undistorted Image', undistorted_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

undistorted_image_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/undistorted_img.jpg'
cv2.imwrite(undistorted_image_path, undistorted_img)

print(f"The undistorted image is saved at: {undistorted_image_path}")
