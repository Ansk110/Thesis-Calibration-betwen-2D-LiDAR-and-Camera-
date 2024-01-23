import numpy as np

def calculate_fov_relative(camera_matrix, marker_size):
    focal_length = (camera_matrix[0, 0] + camera_matrix[1, 1]) / 2.0
    fov_relative = 2 * np.arctan(marker_size / (2 * focal_length))
    fov_degrees = np.degrees(fov_relative)
    return fov_degrees

def main():
    intrinsic_data = np.load('intrinsic_params.npz')
    camera_matrix = intrinsic_data['camera_matrix']
    marker_size = 75.0 
    fov_relative = calculate_fov_relative(camera_matrix, marker_size)
    print("Estimated FOV (relative to marker size):", fov_relative, "degrees")

if __name__ == "__main__":
    main()
