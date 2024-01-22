import numpy as np

aruco_size = 10.0  
lidar_to_aruco_distance = 626 
lidar_fov = 360.0  
angular_size_rad = np.arctan2(aruco_size / 2, lidar_to_aruco_distance)
angular_size_deg = np.degrees(angular_size_rad)

azimuth_range_min = 180.0 - angular_size_deg / 2
azimuth_range_max = 180.0 + angular_size_deg / 2

print(f"Azimuth Range: {azimuth_range_min}° to {azimuth_range_max}°")
