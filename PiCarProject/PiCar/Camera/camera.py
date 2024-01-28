from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os

camera = PiCamera()
camera.resolution = (864, 544)
camera.framerate = 32

rawCapture = PiRGBArray(camera, size=(864, 544))
time.sleep(5)

cv2.namedWindow("Frame")

capture_images = False  
image_index = 1

file_path = '/home/pi/Desktop/Thesis/PiCarProject/PiCar/Camera/Images/'

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):    
    image = frame.array

    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('i'):
        capture_images = True

    if key == ord('q') or key == 27:
        break

    if capture_images:
        file_name = f'img_{image_index}.jpg'
        full_file_path = os.path.join(file_path, file_name)
        cv2.imwrite(full_file_path, image)  
        print("Image captured and saved at:", full_file_path)
        image_index += 1
        capture_images = False 

    rawCapture.truncate(0)

camera.close()
cv2.destroyAllWindows()
