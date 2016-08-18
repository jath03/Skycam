#!/usr/bin/python3 -i
import os, tty, time, threading, gpiozero, sys, termios, curtsies, argparse, colors, picamera
from server import MyServer
from http.server import HTTPServer
#The two endstops are defined as buttons
endstop_front = gpiozero.Button(12)
endstop_back = gpiozero.Button(7)
#The 4 servos(drive controlls 2) are defined as PWMOutputDevices
drive = gpiozero.PWMOutputDevice(2, frequency=300)
pan = gpiozero.PWMOutputDevice(3, frequency=300)
tilt = gpiozero.PWMOutputDevice(4, frequency=300)
#The 4 RGB LEDs are wired together so can be defined as one
leds = gpiozero.RGBLED(24, 25, 8)
leds.on()
#Defining the LEDs colors
red = 0, 1, 1
green = 1, 0, 1
blue = 1, 1, 0
yellow = .1, .5, 1
#adding the argument parser
parser = argparse.ArgumentParser(description='Control the Skycam')
parser.add_argument('-p', '--public', action='store_true', default=False, help='Makes the skycam stream availible over the internet')
parser.add_argument('-s', '--secret', action='store_true', default=False, help='Makes the skycam more secretive')
try:
    args = parser.parse_args()
except:
    sys.exit(1)
class Skycam:
    def __init__(self):
        if args.secret != True:
            leds.blink(on_time=.2, off_time=.2, on_color=green, off_color=blue)
            server_thread = threading.Thread(target = self.run)
            stop_thread = threading.Thread(target=self.collision)
            cam_flip_thread = threading.Thread(target=self.flip)
            os.system('cd /home/jack/mjpg-streamer/mjpg-streamer-experimental && ./mjpg_streamer -i "./input_raspicam.so -fps 10" -o "./output_http.so -w .www -p 8081" &')
            os.system('sudo -u jack motion')
            stop_thread.start()
            server_thread.start()
            cam_flip_thread.start()
            print('Initialized')
            time.sleep(1)
            leds.color = green
        else:
            server_thread = threading.Thread(target=self.run)
            stop_thread = threading.Thread(target=self.collision)
            cam_flip_thread = threading.Thread(target=self.flip)
            os.system('cd /home/jack/mjpg-streamer/mjpg-streamer-experimental && ./mjpg_streamer -i "./input_raspicam.so -fps 10" -o "./output_http.so -w .www -p 8081" &')
            os.system('sudo -u jack motion')
            stop_thread.start()
            server_thread.start()
            cam_flip_thread.start()
            print('Initialized')
            
    def center(self):
        pan.value = .15
        tilt.value = .7
    def off(self):
        pan.off()
        tilt.off()
        drive.off()
    def control(self):
        with curtsies.Input() as k:
            for key in k:
                try:
                    if key == 'w':
                        tilt.value = tilt.value + .02
                        #print('moved')
                        #break
                    elif key == 's':
                        tilt.value = tilt.value - .02
                        #print('moved')
                        #break
                    elif key == 'a':
                        pan.value = pan.value - .02
                        #print('moved')
                        #break
                    elif key == 'd':
                        pan.value = pan.value + .02
                        #print('moved')
                        #break
                    elif key == '<UP>':
                        drive.value = .5
                    elif key == '<DOWN>':
                        drive.value = .3
                    elif key == 'c':
                        self.center()
                    elif key == '<BACKSPACE>':
                        self.off()
                        break
                    else:
                        self.off()
                except gpiozero.exc.OutputDeviceBadValue:
                    if args.secret != True:
                        leds.value = red
                        self.center()   
                        time.sleep(.5)
                        leds.value = green   
                    else:
                        self.center()
    def collision(self):
        print('there was a collision')
        while True:
            if args.secret != True:
                if endstop_front.value == True:
                    leds.color = yellow
                    print('you have hit something in the front')
                    drive.value = .3
                    time.sleep(.5)
                    drive.off()
                    leds.color = green
                elif endstop_back.value == False:
                    leds.color = yellow
                    print('You have hit somthing in the back')
                    drive.value = .5
                    time.sleep(.5)
                    drive.off()
                    leds.color = green
            else:
                 if endstop_front.value == True:
                    print('you have hit something in the front')
                    drive.value = .3
                    time.sleep(.5)
                    drive.off()
                 elif endstop_back.value == False:
                    print('You have hit somthing in the back')
                    drive.value = .5
                    time.sleep(.5)
                    drive.off()
    def run(self):
        print('starting server')
        if args.public == True:
            print(colors.red('Going public'))
            server_address = ('192.168.1.200', 7777)
            httpd = HTTPServer(server_address, MyServer.MyHandler)
            httpd.serve_forever()
        else:
            print(colors.green('Staying private'))
            server_address = ('192.168.1.200', 80)
            httpd = HTTPServer(server_address, MyServer.MyHandler)
            httpd.serve_forever()
    def flip(self):
        while True:
            if tilt.value == .35:
                cam = picamera.PiCamera()
                cam.vflip()                    
def end():
    try:
        os.system('killall motion')
        sys.exit()
    except:
        sys.exit()
