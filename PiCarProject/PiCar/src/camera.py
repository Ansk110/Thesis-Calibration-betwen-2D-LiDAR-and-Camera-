import cv2


def load_image(path):
    img = cv2.imread(str(path))
    return img


def undistort_image(img, cam_mat, dist_coeffs):
    img_shape = img.shape[:2]
    new_cam_mat, roi = cv2.getOptimalNewCameraMatrix(cam_mat, dist_coeffs, img_shape, 1, img_shape)
    dst = cv2.undistort(img, cam_mat, dist_coeffs, None, new_cam_mat)
    return dst
