import os
from math import cos, sin, pi, floor
import pygame
from adafruit_rplidar import RPLidar
from sklearn.cluster import DBSCAN
import numpy as np

class LidarScanner:
    def __init__(self):
        # Set up pygame and the display
        os.putenv('SDL_FBDEV', '/dev/fb1')
        pygame.init()
        self.lcd = pygame.display.set_mode((320, 240))
        pygame.mouse.set_visible(False)
        self.lcd.fill((0, 0, 0))
        pygame.display.update()

        # Setup the RPLidar
        PORT_NAME = '/dev/ttyUSB0'
        self.lidar = RPLidar(None, PORT_NAME)
        self.MAX_DISTANCE = 0

    def process_data(self, data, distance_range, angle_range):
        max_distance = max(distance_range)  # Maximum distance for normalization
        self.lcd.fill((0, 0, 0))

        # Extract valid points within specified distance and angle range
        valid_points = []
        for angle in range(angle_range[0], angle_range[1]):
            distance = data[angle]
            if distance_range[0] <= distance <= distance_range[1]:
                radians = angle * pi / 180.0
                x = distance * cos(radians)
                y = distance * sin(radians)
                valid_points.append([x, y])

        # Convert valid points to numpy array for clustering
        valid_points = np.array(valid_points)

        # Apply DBSCAN clustering
        db = DBSCAN(eps=5, min_samples=10).fit(valid_points)
        labels = db.labels_

        # Assign different colors to different clusters
        colors = {}
        for i, label in enumerate(labels):
            if label == -1:  # Noise points (not part of any cluster)
                color = pygame.Color(255, 255, 255)  # White
            else:
                if label not in colors:
                    colors[label] = pygame.Color(*np.random.randint(0, 256, size=3))  # Random color for each cluster
                color = colors[label]

            # Map points to screen coordinates and display
            x, y = valid_points[i]
            point = (160 + int(x / max_distance * 119), 120 + int(y / max_distance * 119))
            self.lcd.set_at(point, color)

        pygame.display.update()

    def run_lidar(self):
        scan_data = [0] * 360

        # Define the parameters for the box (10x10x10)
        angle_range_box = (0, 360)  # Consider the full 360-degree range
        min_distance_box = 100  # Define the minimum distance for the box
        max_distance_box = 200  # Define the maximum distance for the box

        try:
            print(self.lidar.info)
            for scan in self.lidar.iter_scans():
                for (_, angle, distance) in scan:
                    scan_data[min([359, floor(angle)])] = distance
                self.process_data(scan_data, (min_distance_box, max_distance_box), angle_range_box)

        except KeyboardInterrupt:
            pass  # Continue to the cleanup phase if the user interrupts with Ctrl+C

        finally:
            self.lidar.stop()
            self.lidar.disconnect()
            print("LiDAR Disconnected.")

if __name__ == "__main__":
    lidar_scanner = LidarScanner()
    lidar_scanner.run_lidar()
