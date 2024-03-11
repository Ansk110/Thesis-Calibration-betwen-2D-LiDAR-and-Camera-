import numpy as np

# File path
lidar_filename = "lidar_data.npy"

# Load LiDAR data
lidar_data = np.load(lidar_filename, allow_pickle=True)
if lidar_data is None:
    print("Error: Unable to load LiDAR data.")
else:
    print("LiDAR data loaded successfully.")
    print("LiDAR data:")
    print(lidar_data)
