import numpy as np
import cv2 as cv
import glob

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
parameters = cv.aruco.DetectorParameters_create()

objpoints = []  
imgpoints = []  

images = glob.glob('/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Images/img_1.jpg')
for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    corners, ids, _ = cv.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        for corner in corners:
            cv.cornerSubPix(gray, corner, winSize=(11, 11), zeroZone=(-1, -1), criteria=criteria)

        cv.aruco.drawDetectedMarkers(img, corners, ids)

        for i in range(len(ids)):
            objp = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], dtype=np.float32)
            objpoints.append(objp)

        imgpoints.extend(corners)

        cv.imshow('img', img)
        cv.waitKey(0)

cv.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

np.savez("camera_calibration.npz", camera_matrix=mtx, dist_coeffs=dist)
print("The parameter is saved.")
