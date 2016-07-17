import tty, time, threading, gpiozero, sys, termios, server, curtsies
endstop_front = gpiozero.Button(16)
endstop_back = gpiozero.Button(12)
drive = gpiozero.PWMOutputDevice(2, frequency=300)
pan = gpiozero.PWMOutputDevice(3, frequency=300)
tilt = gpiozero.PWMOutputDevice(4, frequency=300)

class Skycam:
    def __init__(self):
        pass
#    def keyInput(self):
#        fd = sys.stdin.fileno()
#        old_settings = termios.togetattr(fd)
#        try:
#            tty.setraw(sys.stdin.fileno())
#            ch = sys.stdin.read(1)
#        finally:
#            termios.tcsetattr(fd, termios.TCSADRIN, old_settings)
#        return ch
    def move(self, Direction=None):
        if Direction == None:
            drive.off()
            key = curtsies.Input()
            while key == '<UP>':
                drive.value = .5
            while key == '<DOWN>':
                drive.value = .3
        elif Direction != None:
            if Direction.lower() == 'forward':
                drive.value = .5
            elif Direction.lower() == 'backward':
                drive.value = .3
            else:
                drive.off()
    def start(self):
        bg_server.start()
                   
