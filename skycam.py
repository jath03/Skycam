from gpiozero import *
endstop_front = Button(20)
endstop_back = Button(16)
drive = PWMOutputDevice(2, frequency=300, initial_value=False)
pan = PWMOutputDevice(3, frequency=300, initial_value=False)
tilt = PWMOutputDevice(4, frequency=300, initial_value=False)
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
    def forward(self, speed=1):
        drive.value = .3
    def backward(self, speed=1):
        drive.value = .5
    def stop(self):
        drive.off()
    def control(self):
        key = Skycam.keyInput()
        print(key)
            
class PanTilt(Skycam):
    def center(self):
        tilt.value = .75
#while True:
#    Skycam.mainloop()
