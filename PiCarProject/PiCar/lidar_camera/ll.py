import os
from math import cos, sin, pi, floor
import pygame
from adafruit_rplidar import RPLidar
import numpy as np
from sklearn.cluster import DBSCAN

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
        max_distance = 0  # Initialize the maximum distance within this scan
        self.lcd.fill((0, 0, 0))
        for angle in range(angle_range[0], angle_range[1]):
            distance = data[angle]
            if distance_range[0] <= distance <= distance_range[1]:
                radians = angle * pi / 180.0
                x = distance * cos(radians)
                y = distance * sin(radians)
                # Update the maximum distance encountered so far
                max_distance = max(max_distance, distance)
                # Adjust the mapping to the screen as needed
                point = (160 + int(x / max_distance * 119), 120 + int(y / max_distance * 119))
                self.lcd.set_at(point, pygame.Color(255, 255, 255))
        pygame.display.update()
        self.MAX_DISTANCE = max_distance  # Update the MAX_DISTANCE attribute

    def identify_clusters(self, data):
        # Prepare data for clustering
        data_points = []
        for angle, distance in enumerate(data):
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)
            data_points.append([x, y])

        # Convert to NumPy array
        data_points = np.array(data_points)

        # DBSCAN clustering
        eps = 10  # Adjust this parameter as needed
        min_samples = 5  # Adjust this parameter as needed
        db = DBSCAN(eps=eps, min_samples=min_samples).fit(data_points)

        # Get cluster labels
        labels = db.labels_

        # Find unique clusters (excluding noise points, labeled as -1)
        unique_labels = set(labels) - {-1}

        # Visualize clusters
        colors = [pygame.Color(np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
                  for _ in range(max(unique_labels) + 1)]

        self.lcd.fill((0, 0, 0))
        for i, label in enumerate(labels):
            if label != -1:  # Skip noise points
                if self.MAX_DISTANCE != 0:  # Check if MAX_DISTANCE is not zero
                    point = (160 + int(data_points[i][0] / self.MAX_DISTANCE * 119),
                             120 + int(data_points[i][1] / self.MAX_DISTANCE * 119))
                    pygame.draw.circle(self.lcd, colors[label], point, 1)

        pygame.display.update()


    def run_lidar(self):
        scan_data = [0] * 360

        # Define the parameters for the box (10x10x10)
        angle_range_box = (0, 360)  # Consider the full 360-degree range
        min_distance_box = 100  # Define the minimum distance for the box
        max_distance_box = 650  # Define the maximum distance for the box

        try:
            print(self.lidar.info)
            for scan in self.lidar.iter_scans():
                for (_, angle, distance) in scan:
                    scan_data[min([359, floor(angle)])] = distance
                self.process_data(scan_data, (min_distance_box, max_distance_box), angle_range_box)
                self.identify_clusters(scan_data)  # Call the cluster identification method

        except KeyboardInterrupt:
            pass  # Continue to the cleanup phase if the user interrupts with Ctrl+C

        finally:
            self.lidar.stop()
            self.lidar.disconnect()
            print("LiDAR Disconnected.")

if __name__ == "__main__":
    lidar_scanner = LidarScanner()
    lidar_scanner.run_lidar()

