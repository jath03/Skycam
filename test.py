from gpiozero import *
import time
front_endstop = Button(12)
back_endstop = Button(7)
while True:
    print('-------------')
    print(front_endstop.value)
    print('-------------')
    print(back_endstop.value)
    print('-------------')
    time.sleep(.5)
