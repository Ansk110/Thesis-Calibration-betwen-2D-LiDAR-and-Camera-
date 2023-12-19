from picamera.array import PiRGBArray
from picamera import PiCamera
from gpiozero import Robot
import cv2
from time import sleep
import numpy as np

def init_robot(left, right):
    assert len(left) == 3 and len(right) == 3, """Invalid initalization of the
    robot, left and right motor must have 3 parameters"""
    robot = Robot(left = left, right = right)
    return robot

def init_camera():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 16
    rawCapture = PiRGBArray(camera, size=(640, 480))
    # allow the camera to warmup
    sleep(0.1)
    
    return camera, rawCapture
    
def draw_marker_image(corners, ids, image):
    # flatten the ArUco IDs list
    ids = ids.flatten()
    # loop over the detected ArUCo corners
    for (markerCorner, markerID) in zip(corners, ids):
        # extract the marker corners (which are always returned in
        # top-left, top-right, bottom-right, and bottom-left order)
        corners = markerCorner.reshape((4, 2))
        (topLeft, topRight, bottomRight, bottomLeft) = corners
        # convert each of the (x, y)-coordinate pairs to integers
        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))
        
        # draw the bounding box of the ArUCo detection
        cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
        cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
        cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
        cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
        # compute and draw the center (x, y)-coordinates of the ArUco
        # marker
        #cX, cY = calculate_center_marker(corners)
        #cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
        # draw the ArUco marker ID on the image
        cv2.putText(image, str(markerID),
            (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (0, 255, 0), 2)

if __name__ == "__main__":

    # Initialize the camera
    camera, rawCapture = init_camera()
    
    # Load the ARUCO Dictenory and Parameters
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    arucoParams = cv2.aruco.DetectorParameters_create()

    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format = "bgr",
                                           use_video_port = True):
        # grab the raw NumPy array representing the image, then initialize 
        # the timestamp and occupied/unoccupied text
        image = frame.array
        
        # show the frame
        key = cv2.waitKey(1) & 0xFF
        
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        
        # detect ARUCO markers in the image
        (corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict,
            parameters=arucoParams)

        # verify *at least* one ArUco marker was detected
        if len(corners) > 0:
            draw_marker_image(corners, ids, image)
            
        cv2.imshow("Image", image)






