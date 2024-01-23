import numpy as np

file_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/Lidar/lidar_data.npz'

loaded_data = np.load(file_path)
lidar_data = loaded_data['lidar_data']

print("Loaded LiDAR Data:")
print(lidar_data)
