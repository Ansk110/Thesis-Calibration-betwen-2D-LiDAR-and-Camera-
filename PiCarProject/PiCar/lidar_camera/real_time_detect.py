import cv2
import numpy as np
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
from adafruit_rplidar import RPLidar
from picamera import PiCamera
from picamera.array import PiRGBArray
from lid_cam.get_lidar_data import *
from lid_cam.process_lidar_data import *
from lid_cam.filter_lidar_data import *


IMG_W, IMG_H = (864, 544)


def plot_obstacle_region(x, y, s):
    plt.scatter(x, y, c=s, s=5, cmap="rainbow")
    

def init_camera():
    camera = PiCamera()
    camera.resolution = (IMG_W, IMG_H)
    camera.framerate = 32
    return camera


def get_continuous_images(camera):
    rawCapture = PiRGBArray(camera, size=camera.resolution)
    # time.sleep(5)
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):    
        image = frame.array
        yield image
        
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q') or key == 27:
            break

        rawCapture.truncate(0)
        

def main():
    camera = init_camera()
    port = '/dev/ttyUSB0'
    lidar = RPLidar(None, port)
    
    cv2.namedWindow("Frame")
    image_gen = get_continuous_images(camera)
    lidar_gen = get_lidar_data(lidar, interval=1)
    for image, lidar_data in zip(image_gen, lidar_gen):
        filtered_data = filter_lidar_data(lidar_data)
        X, Y, S = process_lidar_data(filtered_data)
        frame = image.copy()
        for (x, y, s) in zip(X, Y, S):
            color = (0, int((1-s)*255), int(s*255))
            frame = cv2.circle(frame, (int(x), int(y)), radius=5, color=color, thickness=-1)
        cv2.imshow("Frame", frame)
    
    data2save = filter_lidar_data(lidar_data, max_range=1000)
    np.save("lidar_data.npy", data2save)
    
    lidar.stop()
    camera.close()
    cv2.destroyAllWindows()

    
if __name__ == "__main__":
    main()

