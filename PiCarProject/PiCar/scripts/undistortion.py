import cv2 as cv
import numpy as np
import glob

intrinsic_params_file = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Intrinsic/intrinsic_params_1.npz'
intrinsic_params = np.load(intrinsic_params_file)
camera_matrix = intrinsic_params['camera_matrix']
dist_coeffs = intrinsic_params['dist_coeffs']

images = glob.glob('/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Images/img_1.jpg')

objpoints = []  
imgpoints = []  

rvecs_array = []
tvecs_array = []

for fname in images:
    img = cv.imread(fname)
    h, w = img.shape[:2]

    undistorted_img = cv.undistort(img, camera_matrix, dist_coeffs, None, camera_matrix)

    mapx, mapy = cv.initUndistortRectifyMap(camera_matrix, dist_coeffs, None, camera_matrix, (w, h), 5)
    remapped_img = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

    undistorted_save_path = f'undistorted_{fname}'
    remapped_save_path = f'remapped_{fname}'
    cv.imwrite(undistorted_save_path, undistorted_img)
    cv.imwrite(remapped_save_path, remapped_img)

    print(f"Undistorted image saved to {undistorted_save_path}")
    print(f"Remapped image saved to {remapped_save_path}")

    gray = cv.cvtColor(undistorted_img, cv.COLOR_BGR2GRAY)
    aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
    parameters = cv.aruco.DetectorParameters_create()
    corners, ids, _ = cv.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        for i in range(len(ids)):
            objpoints.append(np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], dtype=np.float32))
            imgpoints.append(corners[i])
            rvec, tvec, _ = cv.aruco.estimatePoseSingleMarkers(corners[i], 1, camera_matrix, dist_coeffs)

            rvecs_array.append(rvec)
            tvecs_array.append(tvec)

mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs_array[i], tvecs_array[i], camera_matrix, dist_coeffs)
    if len(imgpoints2) == len(imgpoints[i]): 
        error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
        mean_error += error
    else:
        print(f"Dimensions mismatch for marker {i + 1}")

print("Mean reprojection error:", mean_error / len(objpoints))
