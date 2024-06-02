import numpy as np
import os


def load_intrinsic_params(data_path, file_number):
    intrinsic_data = np.load(os.path.join(data_path, f'Intrinsic/intrinsic_params_{file_number}.npz'))
    camera_matrix = intrinsic_data['camera_matrix']
    dist_coeffs = intrinsic_data['dist_coeffs']
    return camera_matrix, dist_coeffs


def load_extrinsic_params(data_path, file_number):
    extrinsic_data = np.load(os.path.join(data_path, f'Extrinsic/extrinsic_params_{file_number}.npz'))
    rotation_matrices = extrinsic_data['rotation_matrices']
    translation_vectors = extrinsic_data['translation_vectors']
    euler_angles = extrinsic_data['euler_angles']
    return rotation_matrices, translation_vectors, euler_angles


def main():
    num_images = 18
    data_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera'

    all_camera_matrices = []
    all_dist_coeffs = []
    all_rotation_matrices = []
    all_translation_vectors = []
    all_euler_angles = []

    for i in range(1, num_images + 1):
        intrinsic_camera_matrix, intrinsic_dist_coeffs = load_intrinsic_params(data_path, i)
        extrinsic_rotation_matrices, extrinsic_translation_vectors, extrinsic_euler_angles = load_extrinsic_params(data_path, i)

        all_camera_matrices.append(intrinsic_camera_matrix)
        all_dist_coeffs.append(intrinsic_dist_coeffs)
        all_rotation_matrices.extend(extrinsic_rotation_matrices)
        all_translation_vectors.extend(extrinsic_translation_vectors)
        all_euler_angles.extend(extrinsic_euler_angles)

    avg_camera_matrix = np.mean(all_camera_matrices, axis=0)
    avg_dist_coeffs = np.mean(all_dist_coeffs, axis=0)
    avg_rotation_matrix = np.mean(all_rotation_matrices, axis=0)
    avg_translation_vector = np.mean(all_translation_vectors, axis=0)
    avg_euler_angles = np.mean(all_euler_angles, axis=0)

    np.savez(os.path.join(data_path, 'average_intrinsic_extrinsic_values.npz'),
             avg_camera_matrix=avg_camera_matrix,
             avg_dist_coeffs=avg_dist_coeffs,
             avg_rotation_matrix=avg_rotation_matrix,
             avg_translation_vector=avg_translation_vector,
             avg_euler_angles=avg_euler_angles)
    print("The average values are saved.")


if __name__ == "__main__":
    main()
