import cv2
import numpy as np

K_file_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Intrinsic/intrinsic_params_1.npz'
K_data = np.load(K_file_path)
K = K_data['camera_matrix']

extrinsic_file_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Extrinsic/extrinsic_params_1.npz'
extrinsic_data = np.load(extrinsic_file_path)
R = extrinsic_data['rotation_matrices'].reshape(-1, 3, 3)  
t = extrinsic_data['translation_vectors'][:, :, 0]  
lidar_data_file_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/Lidar/lidar_data.npz'
lidar_data = np.load(lidar_data_file_path)
lidar_points = lidar_data['lidar_data']  

lidar_points = lidar_points.reshape(-1, 3)  

lidar_points_camera = (R @ lidar_points[:, :, None] + t[:, None]).squeeze()

lidar_points_image = K @ lidar_points_camera.T
lidar_points_image /= lidar_points_image[2, :]

image_file_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Images/img_1.jpg'
image = cv2.imread(image_file_path)

cv2.imshow('Camera Image', image)


for i in range(lidar_points_image.shape[1]):
    u, v = int(lidar_points_image[0, i]), int(lidar_points_image[1, i])
    cv2.circle(image, (u, v), 2, (0, 255, 0), -1) 

cv2.imshow('Projected Lidar Points', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
