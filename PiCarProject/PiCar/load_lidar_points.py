import numpy as np

# Load the LiDAR points from the file
lidar_points_array = np.load('lidar_points.npz')['arr_0']

print("Loaded LiDAR points array:")
print(lidar_points_array)