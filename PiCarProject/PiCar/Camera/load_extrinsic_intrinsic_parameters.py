import numpy as np

def load_intrinsic_params():
    intrinsic_data = np.load('intrinsic_params_1.npz')
    camera_matrix = intrinsic_data['camera_matrix']
    dist_coeffs = intrinsic_data['dist_coeffs']
    return camera_matrix, dist_coeffs

def load_extrinsic_params():
    extrinsic_data = np.load('extrinsic_params_1.npz')
    rotation_matrices = extrinsic_data['rotation_matrices']
    translation_vectors = extrinsic_data['translation_vectors']
    euler_angles = extrinsic_data['euler_angles']
    return rotation_matrices, translation_vectors, euler_angles

# Usage example:
intrinsic_camera_matrix, intrinsic_dist_coeffs = load_intrinsic_params()
print("Intrinsic Camera Matrix:")
print(intrinsic_camera_matrix)
print("\nIntrinsic Distortion Coefficients:")
print(intrinsic_dist_coeffs)

rotation_matrices, translation_vectors, euler_angles = load_extrinsic_params()
print("\nRotation Matrices:")
print(rotation_matrices)
print("\nTranslation Vectors:")
print(translation_vectors)
print("\nEuler Angles:")
print(euler_angles)
