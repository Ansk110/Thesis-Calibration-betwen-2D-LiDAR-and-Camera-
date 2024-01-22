
class BrakeCheck:

    def __init__(self):
        pass
    
    def checkEMBrake(self, scandata, state):
        a = 150
        b = 179
        c = 180
        d = 210
        
        if (state == 0): #straight 60°
            a = 150
            b = 179
            c = 180
            d = 210
        elif (state == 1): #straight and/or right 60°
            a = 180
            b = 209
            c = 210
            d = 239
        elif (state == 2): #straight and/or left 60°
            a = 121
            b = 150
            c = 151
            d = 180
        elif (state == 3): #backwards 60°
            a = 330
            b = 0
            c = 1
            d = 30
        elif (state == 4): #backwards and left 60°
            a = 0
            b = 30
            c = 31
            d = 60
        elif (state == 5): #backwards and right 60°
            a = 300
            b = 329
            c = 330
            d = 0
                
        maxDistance = 400 #320 = 10cm
        checklist = []
        checklist.extend(scandata[a:b])
        checklist.extend(scandata[c:d])
        print(scandata)
        print(checklist)
        for index in checklist:
            if (0 < index < maxDistance):
                return True
        return False
