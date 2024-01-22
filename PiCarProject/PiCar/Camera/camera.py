from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera()
camera.resolution = (864, 544)
camera.framerate = 32
<<<<<<< HEAD
rawCapture = PiRGBArray(camera, size=(320, 240))
# allow the camera to warm up
=======
rawCapture = PiRGBArray(camera, size=(864, 544))
>>>>>>> 3d96b8d (Added files)
time.sleep(5)

cv2.namedWindow("Frame")

capture_images = False  

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):    
    image = frame.array

    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('i'):
        capture_images = True

    if key == 27:  
        break

    if capture_images:
        cv2.imwrite(f'captured_image_{time.time()}.jpg', image)  
        print("Image captured.")
        capture_images = False 

    rawCapture.truncate(0)

cv2.destroyAllWindows()
