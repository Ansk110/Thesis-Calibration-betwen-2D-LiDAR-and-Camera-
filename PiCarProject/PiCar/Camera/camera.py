from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (864, 544)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))
# allow the camera to warm up
time.sleep(5)

# create a window to display the camera feed
cv2.namedWindow("Frame")

capture_images = False  # Flag to indicate capturing images

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image
    image = frame.array

    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    # check if the 'i' key is pressed to capture an image
    if key == ord('i'):
        capture_images = True

    # check if 'Esc' key is pressed to quit
    if key == 27:  # 27 is the ASCII code for 'Esc' key
        break

    # capture an image if the flag is set
    if capture_images:
        cv2.imwrite(f'captured_image_{time.time()}.jpg', image)  # Save the captured image with a unique timestamp
        print("Image captured.")
        capture_images = False  # Reset the flag after capturing an image

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

# close the window and release the camera resources
cv2.destroyAllWindows()
