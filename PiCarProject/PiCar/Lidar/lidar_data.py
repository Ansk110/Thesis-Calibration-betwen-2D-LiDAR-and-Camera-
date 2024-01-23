import os
from math import cos, sin, pi, floor
import pygame
import numpy as np
from adafruit_rplidar import RPLidar

# Set up pygame and the display
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
lcd = pygame.display.set_mode((320, 240))
pygame.mouse.set_visible(False)
lcd.fill((0, 0, 0))
pygame.display.update()

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME)

# used to scale data to fit on the screen
max_distance = 0

# pylint: disable=redefined-outer-name,global-statement
def process_data(data):
    global max_distance
    lidar_data = []
    for angle in range(360):
        distance = data[angle]
        if distance > 0:  # ignore initially ungathered data points
            max_distance = max([min([5000, distance]), max_distance])
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)
            point = (x, y)
            lidar_data.append(point)
    return np.array(lidar_data)

scan_data = [0] * 360

try:
    print(lidar.info)
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        lidar_data = process_data(scan_data)

        # Save LiDAR data to .npz file after one rotation
        np.savez('/home/pi/Desktop/Thesis/PiCarProject/PiCar/Lidar/lidar_data.npz', lidar_data=lidar_data)

        print("LiDAR data saved.")
        break  # Stop after one rotation

except KeyboardInterrupt:
    print('Stopping.')

lidar.stop()
lidar.disconnect()
print("LiDAR Disconnected.")
