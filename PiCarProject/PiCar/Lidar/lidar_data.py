import os
from math import cos, sin, pi, floor
import pygame
from adafruit_rplidar import RPLidar

class LidarDisplay:
    def __init__(self):
        os.putenv('SDL_FBDEV', '/dev/fb1')
        pygame.init()
        self.lcd = pygame.display.set_mode((320, 240))
        pygame.mouse.set_visible(False)
        self.lcd.fill((0, 0, 0))
        pygame.display.update()

        self.PORT_NAME = '/dev/ttyUSB0'
        self.lidar = RPLidar(None, self.PORT_NAME)        
        self.desired_start_angle = 150
        self.desired_end_angle = 250
        self.max_display_distance = 440

    def process_data(self, data):
        max_distance = 0
        self.lcd.fill((0, 0, 0))

        for angle in range(360):
            distance = data[angle]
            if distance > 0 and self.desired_start_angle <= angle <= self.desired_end_angle:
                max_distance = max([min([5000, distance]), max_distance])

                if distance <= self.max_display_distance:
                    radians = angle * pi / 180.0
                    x = distance * cos(radians)
                    y = distance * sin(radians)
                    point = (160 + int(x / max_distance * 119), 120 + int(y / max_distance * 119))
                    self.lcd.set_at(point, pygame.Color(255, 255, 255))

        pygame.display.update()

    def start_display(self):
        scan_data = [0] * 360
        running = True

        try:
            print(self.lidar.info)
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            break

                for scan in self.lidar.iter_scans():
                    for (_, angle, distance) in scan:
                        scan_data[min([359, floor(angle)])] = distance
                    self.process_data(scan_data)
                    if not running:
                        break

        except KeyboardInterrupt:
            print('Stopping.')
            self.lidar.stop()
            self.lidar.disconnect()
            print("LiDAR Disconnected.")
            pygame.quit()

if __name__ == "__main__":
    lidar_display = LidarDisplay()
    lidar_display.start_display()

