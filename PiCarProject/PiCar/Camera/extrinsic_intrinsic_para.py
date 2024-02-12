import cv2
import numpy as np
import glob
import os

def calculate_intrinsic_params(images_path, save_path):
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters_create()

    obj_points = []
    img_points = []

    calibration_images = glob.glob(images_path)

    for idx, fname in enumerate(calibration_images, start=1):
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if corners:
            # Assuming the marker size is 12.5 mm
            marker_size = 12.5
            objp = np.array([[0, 0, 0], [marker_size, 0, 0], [marker_size, marker_size, 0], [0, marker_size, 0]], dtype=np.float32)
            obj_points.append(objp)
            #corners_subpix = cv2.cornerSubPix(gray, corners[0], winSize=(11, 11), zeroZone=(-1, -1), 
                                               #criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
            #img_points.append(corners_subpix)
            img_points.append(corners[0])

    ret, camera_matrix, dist_coeffs, _, _ = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

    for idx in range(1, len(calibration_images) + 1):
        np.savez(os.path.join(save_path, f'intrinsic_params_{idx}.npz'), camera_matrix=camera_matrix, dist_coeffs=dist_coeffs)
        print(f"Intrinsic parameters saved to intrinsic_params_{idx}.npz")

def calculate_extrinsic_params(images_path, intrinsic_save_path, extrinsic_save_path):
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    marker_size = 12.5

    intrinsic_params_list = []

    calibration_images = glob.glob(images_path)

    for idx, fname in enumerate(calibration_images, start=1):
        intrinsic_params = np.load(os.path.join(intrinsic_save_path, f'intrinsic_params_{idx}.npz'))
        intrinsic_params_list.append(intrinsic_params)

    for idx, (fname, intrinsic_params) in enumerate(zip(calibration_images, intrinsic_params_list), start=1):
        camera_matrix = intrinsic_params['camera_matrix']
        dist_coeffs = intrinsic_params['dist_coeffs']

        object_points = np.zeros((0, 3), dtype=np.float32)

        for i in range(-6, 7):
            for j in range(-6, 7):
                object_point = np.array([i * marker_size, j * marker_size, 0.0], dtype=np.float32)
                object_points = np.vstack((object_points, object_point))

        image = cv2.imread(fname)

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

                np.savez(os.path.join(extrinsic_save_path, f'extrinsic_params_{idx}.npz'), rotation_matrices=rotation_matrices,
                         translation_vectors=translation_vectors, euler_angles=euler_angles)
                print(f"Extrinsic parameters saved to extrinsic_params_{idx}.npz")
            else:
                print(f"No markers detected in the image {fname}")
        else:
            print(f"Error: Unable to load the image at '{fname}'")

def main():
    images_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Images/img_*.jpg' 
    intrinsic_save_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Intrinsic'
    extrinsic_save_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Extrinsic'

    calculate_intrinsic_params(images_path, intrinsic_save_path)
    calculate_extrinsic_params(images_path, intrinsic_save_path, extrinsic_save_path)

if __name__ == "__main__":
    main()
