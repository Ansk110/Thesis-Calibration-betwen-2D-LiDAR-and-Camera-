import numpy as np

from .transform import find_x_coordinate


def get_calibration_points(marker_corners, lidar_points):
    lidar_left_point, lidar_right_point = lidar_points
    top_left, top_right, bot_right, bot_left = marker_corners
    paired_points = [
        (top_left, bot_left, lidar_left_point),
        (top_right, bot_right, lidar_right_point),
    ]
    cal_points = []
    for corner_point_a, corner_point_b, lidar_point in paired_points:
        lidar_x, lidar_y = lidar_point
        line_x = find_x_coordinate(corner_point_a, corner_point_b, lidar_y)
        cal_point = [line_x, lidar_y]
        cal_points.append(cal_point)
    return np.array(cal_points)


def get_calibration_error(cal_points: np.array, lidar_points: np.array) -> float:
    return np.linalg.norm(cal_points - lidar_points, axis=1).sum()
