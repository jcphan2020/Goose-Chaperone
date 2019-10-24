#Defines a class that handles location and bearing from
#GPS and (possibly) magnometer data

import threading

class Location (threading.Thread):
    X = 0.0#Current state X coordinate
    Y = 0.0#Current state Y coordinate
    Bearing = 0.0#Degree bearing

    BufferSize = 30#Default buffer size
    LocBuffer = []#Empty location distrobution buffer

    gps_thread=None
    _gps_lambda = ()#GPS method for collecting data
    _bufferIndex = 0

    def __init__(self, bufferSize, gps):
        self.BufferSize = bufferSize
        self.LocBuffer = [(0,0)] * self.BufferSize
        self._gps_lambda = gps
        threading.Thread.__init__(self)

    #Start GPS monitoring
    def start(self):
        gps_thread = threading.Thread(target=self._gps_lambda)
        gps_thread.start()

    #Add next GPS coordinate to queue, determine precise average location
    def addGpsCoord(self, X, Y):
        print(X,Y)
        self._bufferIndex += 1
        if (self._bufferIndex == self.BufferSize):
            self._bufferIndex = 0

    #Use GPS Buffer to determine direction if moving
    def updateBearing(self):
        print("Update Bearing")

    

    #def pause(self): Figure out a semaphore solution
    #    gps_thread.

