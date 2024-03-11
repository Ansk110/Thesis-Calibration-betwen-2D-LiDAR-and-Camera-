import numpy as np

# Function to project LiDAR points onto camera coordinates
def project_lidar_to_camera(lidar_points, camera_intrinsics, camera_extrinsics, lidar_offset):
    # Assuming lidar_points is a numpy array of shape (N, 2) containing 2D LiDAR points
    # camera_intrinsics and camera_extrinsics are numpy arrays representing the camera intrinsic and extrinsic parameters
    # lidar_offset is the offset of the LiDAR from the camera

    # Apply transformation from LiDAR to camera coordinates
    # Translation: Apply the offset of the LiDAR from the camera
    translation_matrix = np.array([[1, 0, 0, lidar_offset[0]],
                                   [0, 1, 0, lidar_offset[1]],
                                   [0, 0, 1, 0],
                                   [0, 0, 0, 1]])

    # Combine intrinsic and extrinsic camera parameters
    camera_matrix = np.dot(camera_intrinsics, camera_extrinsics)

    # Projection matrix (Camera intrinsic-extrinsic parameters)
    projection_matrix = np.dot(camera_matrix, translation_matrix)

    # Homogeneous coordinates for LiDAR points (Adding 1 as z coordinate)
    lidar_points_homogeneous = np.hstack((lidar_points, np.ones((lidar_points.shape[0], 1))))

    # Project LiDAR points onto camera coordinates
    camera_points_homogeneous = np.dot(projection_matrix, lidar_points_homogeneous.T).T

    # Normalize homogeneous coordinates
    camera_points = camera_points_homogeneous[:, :2] / camera_points_homogeneous[:, 2:]

    return camera_points

# Example usage
if __name__ == "__main__":
    # Assuming you have the intrinsic and extrinsic camera parameters
    camera_intrinsics = np.array([[focal_length_x, 0, principal_point_x],
                                   [0, focal_length_y, principal_point_y],
                                   [0, 0, 1]])

    camera_extrinsics = np.array([[rotation_11, rotation_12, rotation_13, translation_x],
                                   [rotation_21, rotation_22, rotation_23, translation_y],
                                   [rotation_31, rotation_32, rotation_33, translation_z]])

    # LiDAR offset from camera
    lidar_offset = np.array([0.15, -0.05])  # Assuming the LiDAR is 15cm behind and 5cm above the camera

    # LiDAR points (Replace this with your actual LiDAR data)
    lidar_points = np.array([[x1, y1], [x2, y2], ...])

    # Project LiDAR points onto camera coordinates
    camera_points = project_lidar_to_camera(lidar_points, camera_intrinsics, camera_extrinsics, lidar_offset)

    # Print or use the camera points for further processing
    print(camera_points)
