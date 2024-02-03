import numpy as np
import os

def load_intrinsic_params(file_path):
    try:
        intrinsic_data = np.load(file_path)
        camera_matrix = intrinsic_data['camera_matrix']
        dist_coeffs = intrinsic_data['dist_coeffs']
        print("Intrinsic Parameters Loaded Successfully.")
        return camera_matrix, dist_coeffs
    except FileNotFoundError:
        print(f"Error: Intrinsic parameters file not found at '{file_path}'")
        return None, None

def load_extrinsic_params(file_path):
    try:
        extrinsic_data = np.load(file_path)
        rotation_matrices = extrinsic_data['rotation_matrices']
        translation_vectors = extrinsic_data['translation_vectors']
        euler_angles = extrinsic_data['euler_angles']
        print("Extrinsic Parameters Loaded Successfully.")
        return rotation_matrices, translation_vectors, euler_angles
    except FileNotFoundError:
        print(f"Error: Extrinsic parameters file not found at '{file_path}'")
        return None, None, None

def main():
    intrinsic_file_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Intrinsic/intrinsic_params_1.npz'
    extrinsic_file_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Extrinsic/extrinsic_params_1.npz'

    camera_matrix, dist_coeffs = load_intrinsic_params(intrinsic_file_path)
    rotation_matrices, translation_vectors, euler_angles = load_extrinsic_params(extrinsic_file_path)

    # Use the loaded parameters as needed
    if camera_matrix is not None and dist_coeffs is not None:
        print("Camera Matrix:")
        print(camera_matrix)
        print("Distortion Coefficients:")
        print(dist_coeffs)

    if rotation_matrices is not None and translation_vectors is not None and euler_angles is not None:
        print("Rotation Matrices:")
        print(rotation_matrices)
        print("Translation Vectors:")
        print(translation_vectors)
        print("Euler Angles:")
        print(euler_angles)

if __name__ == "__main__":
    main()
