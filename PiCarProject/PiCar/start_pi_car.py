from time import sleep
from gpiozero import Robot, Motor
import pygame
import os
from math import cos, sin, pi, floor
from adafruit_rplidar import RPLidar
pygame.init()

running = True
# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'

lidar = RPLidar(None, PORT_NAME)
# Set up pygame and the display
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
lcd = pygame.display.set_mode((320,240))
pygame.mouse.set_visible(False)
lcd.fill((0,0,0))
pygame.display.update()
 
max_distance = 0
#pylint: disable=redefined-outer-name,global-statement
def process_data(data):
    global max_distance
    lcd.fill((0,0,0))
    for angle in range(150,200):
        distance = data[angle]
        if distance > 0:                  # ignore initially ungathered data points
            max_distance = max([min([500, distance]), max_distance])
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)
            point = (160 + int(x / max_distance * 119), 120 + int(y / max_distance * 119))
            lcd.set_at(point, pygame.Color(255,255, 255))
            #print(distance)
    pygame.display.update()

 
scan_data = [0]*360
 

print(lidar.info)
#Pins where motors are connected at (see Motor controller schaltplan for more)
RightMotor = Motor(24,4,19)
LeftMotor = Motor(22,17,18)

#Initial values for the motors, start motors at no speed
InitRightMotor = 0
InitLeftMotor = 0

#DC Motor values
MotorMax = 0.5 #Full speed
MotorMin = 0 #No speed

# Acceleration value
MotorAccelerationSpeed = 0.3#to be changed as needed

#pygame initialization

#Dictionary containing command values, used to control the motors at the same time; KEY UP, DOWN, LEFT AND RIGHT
CommandValues = {'K_UP':0,
                      'K_DOWN':0,
                      'K_LEFT':0,
                      'K_RIGHT':0,
                      'Break':0
                     }

try:
    print(lidar.info)
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        process_data(scan_data)
        front_scan = scan_data[190]
        right_scan = scan_data[240]
        left_scan =  scan_data[140]     
        
        if (front_scan <= 350.00 or right_scan <= 350.00 or left_scan <= 350.00):
            print('There is obstacle ahead')
            RightMotor.forward(speed=0)
            LeftMotor.forward(speed=0)
        else:
            for event in pygame.event.get():
                # if key down is pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        # both motors decelerating
                        CommandValues['K_DOWN'] = 1
                    if event.key == pygame.K_UP:
                        # both motors accelerating
                        CommandValues['K_UP'] = 1
                    if event.key == pygame.K_RIGHT:
                        # only right motor accelerates
                        CommandValues['K_RIGHT'] = 1
                    if event.key == pygame.K_LEFT:
                        # only left motor accelerates
                        CommandValues['K_LEFT'] = 1

                    if event.key == pygame.K_r:  # Press r to bring to initial values servo and motor
                        RightMotor.forward(speed=0)
                        LeftMotor.forward(speed=0)

                    if event.key == pygame.K_b:
                        CommandValues['Break'] = 1

                    if event.key == pygame.K_ESCAPE: # press esc to exit
                        print("EXIT")
                        running = False

                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_DOWN:
                        CommandValues['K_DOWN'] = 0
                    if event.key == pygame.K_UP:
                        CommandValues['K_UP'] = 0
                    if event.key == pygame.K_RIGHT:  
                        CommandValues['K_RIGHT'] = 0
                    if event.key == pygame.K_LEFT:
                        CommandValues['K_LEFT'] = 0
                    if event.key == pygame.K_b:
                        CommandValues['Break'] = 0

                    # Translate values into motor movements

                if CommandValues['K_RIGHT'] == 1:
                    InitLeftMotor = InitLeftMotor + MotorAccelerationSpeed
                    if InitLeftMotor >= MotorMax:
                        InitLeftMotor = MotorMax
                    LeftMotor.forward(speed=InitLeftMotor)
                    RightMotor.forward(speed=0)

                if CommandValues['K_LEFT'] == 1:
                    InitRightMotor = InitRightMotor + MotorAccelerationSpeed
                    if InitRightMotor >= MotorMax:
                        InitRightMotor = MotorMax
                    RightMotor.forward(speed=InitRightMotor)
                    LeftMotor.forward(speed=0)

                if CommandValues['K_DOWN'] == 1:
                    InitRightMotor = InitRightMotor - MotorAccelerationSpeed
                    InitLeftMotor = InitLeftMotor - MotorAccelerationSpeed

                    if InitRightMotor <= MotorMin:  # if positional value exeeds the set limit
                        InitRightMotor = MotorMin  # set it back to its limit value
                    if InitLeftMotor <= MotorMin:
                        InitLeftMotor = MotorMin

                    RightMotor.forward(speed=InitRightMotor)
                    LeftMotor.forward(speed=InitLeftMotor)

        if CommandValues['K_UP'] == 1:

            InitRightMotor = InitRightMotor + MotorAccelerationSpeed
            InitLeftMotor = InitLeftMotor + MotorAccelerationSpeed

            if InitRightMotor >= MotorMax:  # if positional value exeeds the set limit
                InitRightMotor = MotorMax  # set it back to its limit value
            if InitLeftMotor >= MotorMax:
                InitLeftMotor = MotorMax

            RightMotor.forward(speed=InitRightMotor)
            LeftMotor.forward(speed=InitLeftMotor)
            
            
except KeyboardInterrupt:
    print('Stoping.')
pygame.quit()
lidar.stop()
lidar.disconnect()
