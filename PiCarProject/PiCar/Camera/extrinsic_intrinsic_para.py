import cv2
import numpy as np
import glob

def calculate_intrinsic_params(images_path):
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters_create()

    obj_points = []
    img_points = []

    calibration_images = glob.glob(images_path)

    for fname in calibration_images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if corners:
            objp = np.array([[0, 0, 0], [0.04, 0, 0], [0.04, 0.04, 0], [0, 0.04, 0]], dtype=np.float32)
            obj_points.append(objp)
            img_points.append(corners[0])

    ret, camera_matrix, dist_coeffs, _, _ = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)
    np.savez('intrinsic_params_5.npz', camera_matrix=camera_matrix, dist_coeffs=dist_coeffs)

def calculate_extrinsic_params(image_path):
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    marker_size = 0.073

    calibration_data = np.load('intrinsic_params_5.npz')
    camera_matrix = calibration_data['camera_matrix']
    dist_coeffs = calibration_data['dist_coeffs']

    object_points = np.zeros((0, 3), dtype=np.float32)
    for i in range(-6, 7):
        for j in range(-6, 7):
            object_point = np.array([i * marker_size, j * marker_size, 0.0], dtype=np.float32)
            object_points = np.vstack((object_points, object_point))

    image = cv2.imread(image_path)
    if image is not None:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        corners, marker_ids, _ = cv2.aruco.detectMarkers(gray_image, aruco_dict)

        if corners:
            image_points = np.array(corners).squeeze()
            rotation_matrices = []
            translation_vectors = []
            euler_angles = []

            for i in range(len(corners)):
                ret, rotation_vector, translation_vector = cv2.aruco.estimatePoseSingleMarkers(corners[i], marker_size,
                                                                                                camera_matrix, dist_coeffs)

                rotation_matrix, _ = cv2.Rodrigues(rotation_vector)

                roll = np.arctan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
                pitch = np.arctan2(-rotation_matrix[2, 0], np.sqrt(rotation_matrix[2, 1] ** 2 + rotation_matrix[2, 2] ** 2))
                yaw = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])

                rotation_matrices.append(rotation_matrix)
                translation_vectors.append(translation_vector)
                euler_angles.append([roll, pitch, yaw])

            np.savez('extrinsic_params_5.npz', rotation_matrices=rotation_matrices,
                     translation_vectors=translation_vectors, euler_angles=euler_angles)
            print("Extrinsic parameters saved to extrinsic_params.npz")
        else:
            print("No markers detected in the image.")
    else:
        print(f"Error: Unable to load the image at '{image_path}'")

def main():
    images_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Images/img_5.jpg'  # Adjust this path
    calculate_intrinsic_params(images_path)

    image_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Images/img_5.jpg'  # Replace with your image path
    calculate_extrinsic_params(image_path)

if __name__ == "__main__":
    main()
