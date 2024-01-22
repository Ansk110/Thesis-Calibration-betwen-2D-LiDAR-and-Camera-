import os
import pygame
from adafruit_rplidar import RPLidar
import numpy as np


azimuth_range_min = 170
azimuth_range_max = 190

class LidarScanner:
    def __init__(self, port_name='/dev/ttyUSB0'):
        self.exit_program = False
        self.scan_data = [0] * 360
        self.lidar = RPLidar(None, port_name)
        self.initialize_display()

    def initialize_display(self):
        os.putenv('SDL_FBDEV', '/dev/fb1')
        pygame.init()
        self.lcd = pygame.display.set_mode((320, 240))
        pygame.mouse.set_visible(False)
        self.lcd.fill((0, 0, 0))
        pygame.display.update()

    def process_data(self, data):
        max_distance = 1000  
        aruco_angle_range = (azimuth_range_min, azimuth_range_max)
        lidar_points = []

        for angle in range(*aruco_angle_range):
            distance = data[angle]
            if 0 < distance < max_distance:
                radians = angle * np.pi / 180.0
                x = distance * np.cos(radians)
                y = distance * np.sin(radians)
                z = 0  # Assuming lidar is mounted horizontally, adjust if needed
                lidar_points.append([x, y, z, 1])

        lidar_points = np.array(lidar_points)
        return lidar_points

    def run_lidar(self):
        try:
            print(self.lidar.info)
            while True:
                for scan in self.lidar.iter_scans():
                    for (_, angle, distance) in scan:
                        self.scan_data[min([359, int(angle)])] = distance
                    lidar_points = self.process_data(self.scan_data)

                    print("Lidar Points:")
                    print(lidar_points)

        except KeyboardInterrupt:
            print('Stopping.')
        self.lidar.stop()
        self.lidar.disconnect()
        print("LiDAR Disconnected.")

if __name__ == "__main__":
    lidar_scanner = LidarScanner()
    lidar_scanner.run_lidar()
