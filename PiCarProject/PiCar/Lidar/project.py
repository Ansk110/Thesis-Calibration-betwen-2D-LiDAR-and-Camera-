import cv2
import numpy as np

# Example lidar data in homogeneous coordinates (x, y, z)
lidar_points = np.array([[-6.34007708e+02,  6.66368953e+01,  0.00000000e+00,  1.00000000e+00],
                         [-6.26855514e+02,  5.48427511e+01,  0.00000000e+00,  1.00000000e+00],
                         [-6.27467788e+02,  4.38768220e+01,  0.00000000e+00,  1.00000000e+00],
                         [-6.26140718e+02,  3.28146446e+01,  0.00000000e+00,  1.00000000e+00],
                         [-6.27117744e+02,  2.18994342e+01,  0.00000000e+00,  1.00000000e+00],
                         [-6.28154314e+02,  1.09644743e+01,  0.00000000e+00,  1.00000000e+00],
                         [-6.27750000e+02,  7.68772028e-14,  0.00000000e+00,  1.00000000e+00],
                         [-6.27904353e+02, -1.09601112e+01,  0.00000000e+00,  1.00000000e+00],
                         [-6.31115307e+02, -2.20390322e+01,  0.00000000e+00,  1.00000000e+00],
                         [-6.32132495e+02, -3.31286603e+01,  0.00000000e+00,  1.00000000e+00]])

# Example camera intrinsic matrix
camera_matrix = np.array([[1.33193427e+03, 0.00000000e+00, 4.31500000e+02],
                          [0.00000000e+00, 1.13466188e+03, 2.71500000e+02],
                          [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

# Example camera extrinsic matrix (from calibration)
rotation_matrix = np.array([[ 0.94457562, -0.31918981, -0.00496451],
                            [ 0.31906824,  0.9440939,  -0.01342696],
                            [ 0.00917077,  0.01106175,  0.99946539]])

translation_vector = np.array([[0.0365, 0.0365, 0.]])

# Transform lidar points to lidar's coordinate system
lidar_to_lidar_coordinates = np.array([[1, 0, 0, 0],
                                       [0, 1, 0, 0],
                                       [0, 0, 1, 0],
                                       [0, 0, 0, 1]])

lidar_points_lidar_coords = np.dot(lidar_to_lidar_coordinates, lidar_points.T).T

# Transform lidar points to camera coordinates
lidar_to_camera_coordinates = np.concatenate((rotation_matrix, translation_vector.T), axis=1)
lidar_points_camera = np.dot(lidar_to_camera_coordinates, lidar_points_lidar_coords.T).T

# Project lidar points onto image
projected_points = np.dot(camera_matrix, lidar_points_camera.T).T

# Normalize homogeneous coordinates with a check for division by zero
mask = projected_points[:, 2] != 0
projected_points[mask, :2] /= projected_points[mask, 2, None]

# Visualize: Draw lidar points on the image
image = cv2.imread("/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/img_0.jpg")
for point in projected_points:
    cv2.circle(image, (int(point[0]), int(point[1])), 2, (0, 255, 0), -1)

# Display the image with projected lidar points
cv2.imshow("Lidar Projection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
