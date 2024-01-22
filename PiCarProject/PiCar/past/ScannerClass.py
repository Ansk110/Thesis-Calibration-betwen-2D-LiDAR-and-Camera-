from math import floor
import os
from adafruit_rplidar import RPLidar
from threading import Thread

class LidarClass(Thread):
    
    scanData = [0]*360 #create an array/list of the size of 360
    PORT_NAME = '/dev/ttyUSB0'
    lidar = RPLidar(None, PORT_NAME) #create an object named lidar of the class RPLidar() -> adafruit_rplidar library
    
    def __init__(self):
        Thread.__init__(self)
        
    def run(self):
        print(self.lidar.health)
        print(self.lidar.info)
        for scan in self.lidar.iter_scans():
            for (_, angle, distance) in scan:
                self.scanData[min([359, floor(angle)])] = distance
        self.lidar.stop()
        self.lidar.disconnect() 
        