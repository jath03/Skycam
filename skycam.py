import tty
import time
import threading
import gpiozero
import sys
import termios
import server
endstop_front = gpiozero.Button(16)
endstop_back = gpiozero.Button(12)
drive = gpiozero.PWMOutputDevice(2, frequency=300)
pan = gpiozero.PWMOutputDevice(3, frequency=300)
tilt = gpiozero.PWMOutputDevice(4, frequency=300)

class Skycam:
    def keyInput(self):
        fd = sys.stdin.fileno()
        old_settings= termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    def mainloop(self):
        Drive.control()
        
        
class Drive(Skycam):
    def __init__(self):
        stop_thread = threading.Thread(target=self.end())
        stop_thread.start()
    def forward(self, speed=1):
        drive.value = .3
    def backward(self, speed=1):
        drive.value = .5
    def stop(self):
        drive.off()
    def control(self):
        while True:
            key = Skycam.keyInput()
            if key == 'Up':
                self.forward()
            elif key == 'Down':
                self.backward()
    def end(self):
        while endstop_front.value or endstop_back.value == True:
            self.stop()
            
class PanTilt(Skycam):
    def center(self):
        tilt.value = .75
def webinterface():
    dr = drive.value
    pn = pan.value
    tlt = tilt.value
    return dr, pn, tlt
   
drive_thread = threading.Thread(target=Drive.control(Drive))
drive_thread.start()
bg_server.start()

