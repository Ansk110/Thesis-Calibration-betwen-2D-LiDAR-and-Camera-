import pygame
from gpiozero import Motor

class Steering:
     
    def __init__(self):
        self.Vr = 0.2
        self.Vl = 0.2
        self.Vmax = 0.35
        self.Vmin = 0.17
        self.distanceMin = 450
        self.manualAcc = 0.05
        self.autonomusAcc = 0.07
        self.RightMotor = Motor(4,24,19) 
        self.LeftMotor = Motor(17,22,18)
        self.commandValues = {'K_UP':0,
                          'K_DOWN':0,
                          'K_LEFT':0,
                          'K_RIGHT':0,
                          'Break':0
                         }
    def driveManual(self,event):
        self.getKeyEvents(event)
        self.drive()
        
        
    def driveAutonomus(self,scanData):
        self.checkScanData(scanData)
        #self.drive()
        
    
    
    def checkScanData(self,scanData):
        if min(scanData[140:240]) < 350 and min(scanData[140:240]) > 0:
            print("We are changing direction")
            # This is  left
            if (min(scanData[241:300]) < 450 and min(scanData[241:300]) > 0) and (min(scanData[80:139]) > 450 and min(scanData[80:139]) > 0):
                self.Vr += self.manualAcc
                self.Vl -= self.manualAcc
                if self.Vr > self.Vmax:
                    self.Vr = self.Vmax
                if self.Vl < self.Vmin:
                    self.Vl = self.Vmin
            # This is  right
            if (min(scanData[241:300]) > 450 and min(scanData[241:300]) > 0) and (min(scanData[80:139]) < 450 and min(scanData[80:139]) > 0):
                print("Go to Right")
                self.Vr -= self.manualAcc
                self.Vl += self.manualAcc
                if self.Vr < self.Vmin:
                    self.Vr = self.Vmin
                if self.Vl > self.Vmax:
                    self.Vl = self.Vmax
            if (min(scanData[241:300]) > 450 and min(scanData[241:300]) > 0) and (min(scanData[80:139]) > 450 and min(scanData[80:139]) > 0):
                print("Go to Right")
            if (min(scanData[241:300]) < 450 and min(scanData[241:300]) > 0) and (min(scanData[80:139]) < 450 and min(scanData[80:139]) > 0):
                print("Go to Back")
        else:
            self.Vr = 0.2
            self.Vl = 0.2
            print("You have to move forward") 
        self.RightMotor.forward(speed=self.Vr)
        self.LeftMotor.forward(speed=self.Vl)
    def drive(self):
        if self.commandValues['K_UP'] == 1:
            print("We are goint Fast")
            if(self.Vr != self.Vl):
                self.Vl = self.Vr
            self.Vr += self.manualAcc
            self.Vl += self.manualAcc
            if self.Vr > self.Vmax:
                self.Vr = self.Vmax
            if self.Vl > self.Vmax:
                self.Vl = self.Vmax
        elif self.commandValues['K_DOWN'] == 1:
            print("We are goinng slow")
            if(self.Vr != self.Vl):
                self.Vl = self.Vr
            self.Vr -= self.manualAcc
            self.Vl -= self.manualAcc
            if self.Vr < self.Vmin:
                self.Vr = self.Vmin
            if self.Vl < self.Vmin:
                self.Vl = self.Vmin
        elif self.commandValues['K_LEFT'] == 1:
            print("We are goinng Left")
            self.Vr += self.manualAcc
            self.Vl -= self.manualAcc
            if self.Vr > self.Vmax:
                self.Vr = self.Vmax
            if self.Vl < self.Vmin:
                self.Vl = self.Vmin
        elif self.commandValues ['K_RIGHT'] == 1:
            print("We are goinng Right")
            self.Vr -= self.manualAcc
            self.Vl += self.manualAcc
            if self.Vr < self.Vmin:
                self.Vr = self.Vmin
            if self.Vl > self.Vmax:
                self.Vl = self.Vmax
        elif self.commandValues['Break'] == 1:
            print("Braking started!!!!!")
            self.Vr = 0.0
            self.Vl = 0.0
        self.RightMotor.forward(speed=self.Vr)
        self.LeftMotor.forward(speed=self.Vl)
         
    def getKeyEvents(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.commandValues['K_UP'] = 1
            elif event.key == pygame.K_DOWN:
                self.commandValues['K_DOWN'] = 1
            elif event.key == pygame.K_LEFT:
                self.commandValues['K_LEFT'] = 1
            elif event.key == pygame.K_RIGHT:
                self.commandValues['K_RIGHT'] = 1
            elif event.key == pygame.K_b:
                self.commandValues['Break'] = 1
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.commandValues['K_UP'] = 0
            elif event.key == pygame.K_DOWN:
                self.commandValues['K_DOWN'] = 0
            elif event.key == pygame.K_LEFT:
                self.commandValues['K_LEFT'] = 0
            elif event.key == pygame.K_RIGHT:
                self.commandValues['K_RIGHT'] = 0
            elif event.key == pygame.K_b:
                self.commandValues['Break'] = 0
    

    
    