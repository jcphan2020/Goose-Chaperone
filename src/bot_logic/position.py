#Defines a class that handles location and bearing from
#GPS and (possibly) magnometer data

import threading

class Location (threading.Thread):
    X = 0.0#Current state X coordinate
    Y = 0.0#Current state Y coordinate
    Bearing = 0.0#Degree bearing

    BufferSize = 30#Default buffer size
    LocBuffer = []#Empty location distrobution buffer
    _gps_lambda = ()#GPS method for collecting data
    gps_thread=None

    def __init__(self, bufferSize, gps):
        self.BufferSize = bufferSize
        self.LocBuffer = [(0,0)] * self.BufferSize
        self._gps_lambda = gps
        threading.Thread.__init__(self)

    def start(self):
        gps_thread = threading.Thread(target=self._gps_lambda)
        gps_thread.start()

