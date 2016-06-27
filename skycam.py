from gpiozero import *
endstop_front = Button(20)
endstop_back = Button(16)
drive = PWMOutputDevice(2, frequency=50)
pan = PWMOutputDevice(3, frequency=50)
tilt = PWMOutputDevice(4, frequency=50)
class Skycam():
    def forward(self, speed=1):
        drive.value = .3
    def backward(self, speed=1):
        drive.value = .5
    def drive(self):
        pass
    def PanTilt(self):
        pass
        
        
