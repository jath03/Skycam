from gpiozero import *
endstop_front = Button(20)
endstop_back = Button(16)
drive = PWMOutputDevice(4, frequency=50)
pan = PWMOutputDevice(2, frequency=50)
tilt = PWMOutputDevice(3, frequency=50)
class Skycam():
    def forward(self, speed=50):
        drive.value=1
