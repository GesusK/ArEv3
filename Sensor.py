__author__ = 'Arthur'
'''
A set of classes to support basic sensorings with following sensors:
    Gyro sensor;
'''
from ev3.lego import GyroSensor

class Gyro:
    gyro=None;

    def __init__(self):
        self.gyro=GyroSensor();

    def reset(self):
        if (self.gyro == None):
            print "Gyro sensor not set properly."
            return
        self.gyro.rate;

    def readAngle(self,RESET=0):
        if(RESET==1):
            self.gyro.reset();
        return self.gyro.ang;