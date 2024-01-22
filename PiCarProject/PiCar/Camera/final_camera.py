import cv2
import numpy as np

calibration_data = np.load('average_intrinsic_extrinsic_values.npz')
camera_matrix = calibration_data['avg_camera_matrix']
dist_coeffs = calibration_data['avg_dist_coeffs']

aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)  
parameters = cv2.aruco.DetectorParameters_create()

cap = cv2.VideoCapture(0)  

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    
    new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
    undistorted_frame = cv2.undistort(frame, camera_matrix, dist_coeffs, None, new_camera_matrix)
    
    corners, ids, _ = cv2.aruco.detectMarkers(undistorted_frame, aruco_dict, parameters=parameters)

    if corners:        
        undistorted_frame = cv2.aruco.drawDetectedMarkers(undistorted_frame, corners, ids)
        
        for i in range(len(corners)):
            rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.04, camera_matrix, dist_coeffs)
            undistorted_frame = cv2.aruco.drawAxis(undistorted_frame, camera_matrix, dist_coeffs, rvec, tvec, 0.02)

    cv2.imshow('ArUco Marker Detection', undistorted_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
