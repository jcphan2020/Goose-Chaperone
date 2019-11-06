'''
    IO Broker is a data provider to connect to all IO inputs into a 
    registration object to allow the bot to access data as necessary,
    without directly interfacing with component scripts

    Paradigm:
        Register inputs by some contract
        Register outputs (motors) by some contract
        Central logic reads/publishes as needed
'''

class Broker:

    iMotor = None
    iUltraSonic = None
    iCapture = None

    def __init__(self):
        return
    
    #Registration
    def register_Motor(self, motor):
        self.iMotor = motor
    
    def registerUltraSonicSensor(self, sensor):
        self.iUltraSonic = sensor

    def registerCapture(self, capture):
        self.iCapture = capture

    #Configurations
    '''Hazards determined by image recognition, with estimated distance'''
    def SetMinOpticalHazardDistance(self, dist):
        self.iCapture.SetMinHazardDist(dist)

    '''Hazards detected by ultrasonic sensor'''
    def SetMinPhysicalHazardDistance(self, dist):
        self.iUltraSonic.SetMinHazardDist(dist)

    #Contract methods

    #Motor methods
    def SetMotorDir(self, dir):
        self.iMotor.set_dir(dir)

    def SetMotorSpeed(self, speed):
        self.iMotor.set_speed(speed)

    #Ultra sonic methods
    '''Get object distance if within range; None otherwise'''
    def GetDistance(self):
        return self.iUltraSonic.GetDistance()

    #Tensorflow methods
    '''Get list of named bounding boxes'''
    def GetNamedBoundingList(self):
        return self.iCapture.GetNamedBoundingList()

    '''Get list of seen hazards within estimated distance'''
    def GetOpticalHazardDistance(self):
        return self.iCapture.GetHazardCoords()

    

    


