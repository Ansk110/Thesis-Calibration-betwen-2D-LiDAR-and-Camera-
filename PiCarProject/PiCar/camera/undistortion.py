import cv2
import numpy as np
import glob
import os

def undistort_and_remap(images_path, intrinsic_params_path, undistorted_save_path, remapped_save_path):
    intrinsic_params_files = glob.glob(os.path.join(intrinsic_params_path, 'camera_calibration.npz'))
    if not intrinsic_params_files:
        print("No intrinsic parameters files found.")
        return

    intrinsic_params_list = []
    for file_path in intrinsic_params_files:
        intrinsic_params = np.load(file_path)
        intrinsic_params_list.append(intrinsic_params)

    for idx, file_path in enumerate(sorted(glob.glob(images_path)), start=1):
        img = cv2.imread(file_path)
        if img is None:
            print(f"Error: Unable to load the image at '{file_path}'")
            continue

        intrinsic_params = intrinsic_params_list[idx - 1]
        camera_matrix = intrinsic_params['camera_matrix']
        dist_coeffs = intrinsic_params['dist_coeffs']

        h, w = img.shape[:2]
        new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))

        undistorted_img = cv2.undistort(img, camera_matrix, dist_coeffs, None, new_camera_matrix)

        undistorted_filename = os.path.basename(file_path)
        undistorted_save_file_path = os.path.join(undistorted_save_path, f'undistorted_{undistorted_filename}')
        cv2.imwrite(undistorted_save_file_path, undistorted_img)
        print(f"Undistorted image saved: {undistorted_save_file_path}")

        mapx, mapy = cv2.initUndistortRectifyMap(camera_matrix, dist_coeffs, None, new_camera_matrix, (w, h), 5)
        remapped_img = cv2.remap(undistorted_img, mapx, mapy, cv2.INTER_LINEAR)

        remapped_filename = f'remapped_{undistorted_filename}'
        remapped_save_file_path = os.path.join(remapped_save_path, remapped_filename)
        cv2.imwrite(remapped_save_file_path, remapped_img)
        print(f"Remapped image saved: {remapped_save_file_path}")

def main():
    images_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Images/img_1.jpg'
    intrinsic_params_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/camera'
    undistorted_save_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/camera/undistorted_images'
    remapped_save_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/camera/remapped_images'

    undistort_and_remap(images_path, intrinsic_params_path, undistorted_save_path, remapped_save_path)

if __name__ == "__main__":
    main()
