import numpy as np


def euler_to_rotation_matrix(roll_deg, pitch_deg, yaw_deg):
    """
    Compute the rotation matrix from Euler angles (roll, pitch, yaw) using the ZYX convention.
    """
    roll = np.deg2rad(roll_deg)
    pitch = np.deg2rad(pitch_deg)
    yaw = np.deg2rad(yaw_deg)
    # Compute individual rotation matrices
    R_x = np.array([[1, 0, 0],
                    [0, np.cos(roll), -np.sin(roll)],
                    [0, np.sin(roll), np.cos(roll)]])

    R_y = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                    [0, 1, 0],
                    [-np.sin(pitch), 0, np.cos(pitch)]])

    R_z = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                    [np.sin(yaw), np.cos(yaw), 0],
                    [0, 0, 1]])

    # Combine rotation matrices in ZYX order
    return R_z @ R_y @ R_x


def get_extrinsic_matrix(roll_deg, pitch_deg, yaw_deg, x0, y0, z0):
    extrinsic_mat = np.identity(n=4)
    rot_mat = euler_to_rotation_matrix(roll_deg, pitch_deg, yaw_deg)
    extrinsic_mat[:3, :3] = rot_mat
    extrinsic_mat[:3, 3] = np.array([x0, y0, z0])
    return extrinsic_mat


def polar_to_cart_coord(angles, distances):
    # Convert polar into cartesian coordinates
    cart_points = np.zeros(shape=(len(angles), 3))
    rad_angles = np.deg2rad(angles)
    cart_points[:, 0] = distances*np.cos(rad_angles)
    cart_points[:, 1] = distances*np.sin(rad_angles)
    return cart_points


def add_homo_coord(points):
    N = points.shape[0]
    ones = np.ones((N, 1))
    return np.hstack((points, ones))


def scale_and_translate_points(points, scale_mat, trans_vec):
    return points @ scale_mat + trans_vec


def find_x_coordinate(a, b, y):
    # Calculate the slope of the line
    if b[0] == a[0]:
        # Line is a vertical line
        return a[0]

    slope = (b[1] - a[1]) / (b[0] - a[0])

    # Calculate the y-intercept using the point-slope form of the line equation: y - y1 = m(x - x1)
    y_intercept = a[1] - slope * a[0]

    # Calculate the y-coordinate using the slope-intercept form of the line equation: y = mx + b
    # y = slope * x + y_intercept
    x = (y - y_intercept) / slope
    return x