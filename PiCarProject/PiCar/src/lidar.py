import cv2
import numpy as np

from .transform import add_homo_coord, polar_to_cart_coord, scale_and_translate_points


def load_lidar_data(path):
    array = np.load(path)
    return array


def filter_lidar_data(data, max_range=100000, min_angle=158, max_angle=205):
    filtered_data = [point for point in data if point[2] <= max_range and min_angle < point[1] < max_angle]
    return np.array(filtered_data)


def lidar_to_camera_coord(points, extrinsic_mat):
    homo_points = add_homo_coord(points)
    return (extrinsic_mat @ homo_points.T).T[:, :3]


def camera_coord_to_pixel(cam_coord, cam_matrix, dist_coeffs):
    image_points, _ = cv2.projectPoints(cam_coord, np.zeros((3,)), np.zeros((3,)), cam_matrix, dist_coeffs)
    return image_points.squeeze()


def process_lidar_data(raw_points, extrinsic_mat, cam_matrix, dist_coeffs, scale_mat, trans_vec):
    lidar_points = polar_to_cart_coord(angles=raw_points[:, 1], distances=raw_points[:, 2])
    lidar_cam_points = lidar_to_camera_coord(lidar_points, extrinsic_mat=extrinsic_mat)
    lidar_pixels = camera_coord_to_pixel(lidar_cam_points, cam_matrix=cam_matrix, dist_coeffs=dist_coeffs)
    lidar_pixels = scale_and_translate_points(lidar_pixels, scale_mat, trans_vec)
    lidar_pixels = np.round(lidar_pixels).astype(int)
    return lidar_pixels


def get_lidar_terminal_points(lidar_points):
    shortest_distance = lidar_points[:, 1].min()
    obj_lidar_points = lidar_points[lidar_points[:, 1] <= shortest_distance + 10]
    left_point = lidar_points[lidar_points[:, 0] == obj_lidar_points[:, 0].min()][0]
    right_point = lidar_points[lidar_points[:, 0] == obj_lidar_points[:, 0].max()][0]
    return left_point, right_point
