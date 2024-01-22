import cv2
import numpy as np
import glob

aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250) 
parameters = cv2.aruco.DetectorParameters_create()

obj_points = []  
img_points = []  

calibration_images = glob.glob('/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Images/img_5.jpg')

for fname in calibration_images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if corners:        
        img = cv2.aruco.drawDetectedMarkers(img, corners, ids)
        cv2.imshow('img', img)
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            
        objp = np.array([[0, 0, 0], [0.04, 0, 0], [0.04, 0.04, 0], [0, 0.04, 0]], dtype=np.float32)
        obj_points.append(objp)

        img_points.append(corners[0])  

cv2.destroyAllWindows()

ret, camera_matrix, dist_coeffs, _, _ = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

np.savez('intrinsic_params_1.npz', camera_matrix=camera_matrix, dist_coeffs=dist_coeffs)
