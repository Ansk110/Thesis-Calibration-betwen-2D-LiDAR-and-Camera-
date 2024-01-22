import numpy as np

def load_average_values(file_path):
    data = np.load(file_path)
    avg_camera_matrix = data['avg_camera_matrix']
    avg_dist_coeffs = data['avg_dist_coeffs']
    avg_rotation_matrix = data['avg_rotation_matrix']
    avg_translation_vector = data['avg_translation_vector']
    avg_euler_angles = data['avg_euler_angles']
    return (
        avg_camera_matrix,
        avg_dist_coeffs,
        avg_rotation_matrix,
        avg_translation_vector,
        avg_euler_angles,
    )

if __name__ == "__main__":
    file_path = 'average_intrinsic_extrinsic_values.npz'  
    (
        avg_camera_matrix,
        avg_dist_coeffs,
        avg_rotation_matrix,
        avg_translation_vector,
        avg_euler_angles,
    ) = load_average_values(file_path)

    print("Loaded Average Camera Matrix:\n", avg_camera_matrix)
    print("Loaded Average Distortion Coefficients:\n", avg_dist_coeffs)
    print("Loaded Average Rotation Matrix:\n", avg_rotation_matrix)
    print("Loaded Average Translation Vector:\n", avg_translation_vector)
    print("Loaded Average Euler Angles (in radians):\n", avg_euler_angles)
