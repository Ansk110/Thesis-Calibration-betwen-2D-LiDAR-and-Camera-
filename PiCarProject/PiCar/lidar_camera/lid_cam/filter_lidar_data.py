import numpy as np

def filter_lidar_data(data, max_range=100000, min_angle=156, max_angle=205):
    filtered_data = [point for point in data if point[2] <= max_range and min_angle < point[1] < max_angle]
    return np.array(filtered_data)