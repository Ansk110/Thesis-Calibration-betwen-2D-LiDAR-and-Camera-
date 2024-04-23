from .transform import find_x_coordinate


def get_calibration_error(marker_corners, lidar_left_point, lidar_right_point):
    top_left, top_right, bot_right, bot_left = marker_corners
    paired_points = [
        (top_left, bot_left, lidar_left_point),
        (top_right, bot_right, lidar_right_point),
    ]
    cal_error = 0.0
    for corner_point_a, corner_point_b, lidar_point in paired_points:
        lidar_x, lidar_y = lidar_point
        line_x = find_x_coordinate(corner_point_a, corner_point_b, lidar_y)
        cal_error += (line_x - lidar_x)**2
    return cal_error
