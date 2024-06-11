import os
from math import cos, sin, pi, floor
import pygame
from adafruit_rplidar import RPLidar
import time
import cv2

class LidarScanner:
    def __init__(self, port_name='/dev/ttyUSB0'):
        self.exit_program = False
        self.max_distance = 0
        self.scan_data = [0] * 360
        self.lidar = RPLidar(None, port_name)
        self.initialize_display()

    def initialize_display(self):
        os.putenv('SDL_FBDEV', '/dev/fb1')
        pygame.init()
        self.lcd = pygame.display.set_mode((500, 500))
        pygame.mouse.set_visible(False)
        self.lcd.fill((0, 0, 0))
        pygame.display.update()

    def process_data(self, data):
        self.lcd.fill((0, 0, 0))
        for angle in range(360):
            distance = data[angle]
            if distance > 0:
                self.max_distance = max([min([5000, distance]), self.max_distance])
                radians = angle * pi / 180.0
                x = distance * cos(radians)
                y = distance * sin(radians)
                point = (160 + int(x / self.max_distance * 500), 120 + int(y / self.max_distance * 500))
                self.lcd.set_at(point, pygame.Color(255, 255, 255))
        pygame.display.update()

    def distance_at_angle(self, angle, max_distance=1000):
        distance = self.scan_data[angle] if self.scan_data[angle] is not None and self.scan_data[angle] < max_distance else 0
        return distance

    def run_lidar(self):
        try:
            print(self.lidar.info)
            while True:
                for scan in self.lidar.iter_scans():
                    for (_, angle, distance) in scan:
                        self.scan_data[round(angle)] = distance
                    self.process_data(self.scan_data)

                    front_distance = self.distance_at_angle(angle=180)
                    back_distance = self.distance_at_angle(angle=0)
                    left_distance = self.distance_at_angle(angle=90)
                    right_distance = self.distance_at_angle(angle=270)

                    print(f"Front: {front_distance} mm | Back: {back_distance} mm | "
                          f"Left: {left_distance} mm | Right: {right_distance} mm")

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.exit_program = True
                time.sleep(1)

        except KeyboardInterrupt:
            print('Stopping.')
        self.lidar.stop()
        self.lidar.disconnect()
        print("LiDAR Disconnected.")

if __name__ == "__main__":
    lidar_scanner = LidarScanner()
    lidar_scanner.run_lidar()