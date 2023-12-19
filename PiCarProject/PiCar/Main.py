from time import sleep
from ScannerClass import LidarClass
from Stering import Steering
import pygame
from gpiozero import Motor

driving = Steering()
scanner = LidarClass()

pygame.init()
screen = pygame.display.set_mode((100,100))

running = True
scanner.start()
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    driving.driveAutonomus(scanner.scanData)
pygame.quit()