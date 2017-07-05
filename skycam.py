#!/usr/bin/python3.5
from PyQt5.QtCore import QObject, QThread
from communication import Communication
from flask import Flask, Response
from streamer import Streamer, main, FlaskThread
from functools import partial


class Skycam(QObject):
    def __init__(self, master, cam, communication=None):
        super().__init__()
        self.master = master
        if not communication:
            self.comm = Communication(self, 0x50)
        else:
            self.comm = communication
        self.fapp = Flask(__name__)
        self.streamer = Streamer(self, cam)
        @self.fapp.route('/')
        def feed():
            return Response(self.streamer.stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
        self.th = FlaskThread(self.fapp)
        self.th.start()
    def move(self, direction=None):
        '''Moves the Skycam in the direction specified
Usage: Skycam.move(direction)
where direction is either 0 for forward or 1 for backward'''
        if direction is not None:
            self.comm.write("move," + str(direction))
        else:
            self.comm.write("move,-1")
            return int(self.comm.read())
    def pan(self, direction=None):
        '''Pans the Skycam's camera in the direction specified
Usage: Skycam.pan(direction)
where direction is either 0 for right or 1 for left'''
        if direction:
            self.comm.write("pan," + str(direction))
        else:
            self.comm.write("pan,-1")
            return int(self.comm.read())
    def tilt(self, direction):
        '''Tilts the Skycam's camera in the direction specified
Usage: Skycam.tilt(direction)
where direction is either 0 for up or 1 for down'''
        if direction:
            self.comm.write("tilt," + str(direction))
        else:
            self.comm.write("tilt,-1")
            return int(self.comm.read())
    def pan_to(self, angle=None):
        if angle:
            self.comm.write("panto," + str(angle))
        else:
            self.comm.write("panto,-1")
            return int(self.comm.read())
    def tilt_to(self, angle=None):
        if angle:
            self.comm.write("tiltto," + str(angle))
        else:
            self.comm.write("tiltto,-1")
            return int(self.comm.read())

if __name__ == '__main__':
    import cv2
    cam = cv2.VideoCapture(-1)
    sk = Skycam(None, cam)
