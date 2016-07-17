from gpiozero import *
front_endstop = Button(16)
tlt = PWMOutputDevice(4, frequency=200)
