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

# Define the desired horizontal range of the LiDAR in degrees
min_angle = 158    # Minimum angle (inclusive)
max_angle = 201  # Maximum angle (inclusive)

# Define the maximum distance from LiDAR in mm
max_distance = 5500  # 5500 mm (or 550 cm)

# Define the list to store LiDAR points
lidar_points = []

# Define the condition to stop LiDAR collection
max_scans = 10  # Maximum number of scans to collect
scan_count = 0  # Counter to keep track of the number of scans

# pylint: disable=redefined-outer-name,global-statement
def process_data(data):
    global max_distance
    lcd.fill((0, 0, 0))
    for angle in range(len(data)):
        distance = data[angle]
        if min_angle <= angle <= max_angle and distance <= max_distance:  # Check angle and distance
            if distance > 0:  # ignore initially ungathered data points
                max_distance = max([min([5000, distance]), max_distance])
                radians = angle * pi / 180.0
                x = distance * cos(radians)
                y = distance * sin(radians)
                lidar_points.append((x, y))  # Append point to the list
                point_display = (160 + int(x / max_distance * 119), 120 + int(y / max_distance * 119))
                lcd.set_at(point_display, pygame.Color(255, 255, 255))
    pygame.display.update()

scan_data = [0] * 360
try:
    print(lidar.info)
    
    rotation_count = 0  # Counter to track the number of rotations completed
    
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            angle = int(angle) % 360  # Adjust angle to be within the range of 0 to 359 degrees
            if 159.894 <= angle <= 200.105:  # Check if angle is within desired range
                scan_data[angle] = distance
        process_data(scan_data)
        
        rotation_count += 1  # Increment rotation count
        
        # Check if two rotations are completed
        if rotation_count >= 1000:
            break  # Exit the loop if two rotations are completed


except KeyboardInterrupt:
    print('Stopping.')
lidar.stop()
lidar.disconnect()
print("LiDAR Disconnected.")

# Convert lidar_points to a NumPy array
lidar_points_array = np.array(lidar_points)

# Save the LiDAR points to a file (e.g., CSV, XYZ, PLY)
np.savez('lidar_points.npz', lidar_points_array)
print("LiDAR points saved to 'lidar_points.npz'.")
