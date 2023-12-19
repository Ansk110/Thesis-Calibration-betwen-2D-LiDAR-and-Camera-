import cv2 as cv
from cv2 import aruco
import numpy as np


def augmented_reality(frame, image, required_points):
    image_h, image_w = image.shape[:2]
    frame_h, frame_w = frame.shape[:2]
    mask = np.zeros((frame_h, frame_w), dtype=np.uint8)
    corner_points = np.array([[0, 0], [image_w, 0], [image_w, image_h], [0, image_h]])
    matrix, _ = cv.findHomography(srcPoints=corner_points, dstPoints=required_points)
    warping = cv.warpPerspective(image, matrix, (frame_w, frame_h))
    cv.fillConvexPoly(mask, required_points.astype(np.int32), 255)
    results = cv.bitwise_and(warping, warping, frame, mask=mask)


def main():
    dictionary = aruco.Dictionary_get(aruco.DICT_4X4_50)
    param_markers = aruco.DetectorParameters_create()
    image_src = cv.imread("C:/Users/chhet/Desktop/KakaduPark/Kakadu_National_Park.JPG")

    scale_factor = 2
    cap = cv.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        marker_corners, marker_ids, _ = aruco.detectMarkers(gray_frame, dictionary, parameters=param_markers)
        if marker_corners:
            for ids, corners in zip(marker_ids, marker_corners):
                corners = corners.reshape(4, 2)
                corners = corners.astype(int)

                center = np.mean(corners, axis=0)
                offset = int(max(corners[:, 0].max() - corners[:, 0].min(), corners[:, 1].max() - corners[:, 1].min()) * (scale_factor - 1) / 2)
                enlarged_corners = np.array([[center[0] - offset, center[1] - offset],
                                             [center[0] + offset, center[1] - offset],
                                             [center[0] + offset, center[1] + offset],
                                             [center[0] - offset, center[1] + offset]])

                augmented_reality(frame, image_src, enlarged_corners)
        cv.imshow("frame", frame)
        key = cv.waitKey(1)
        if key == ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
