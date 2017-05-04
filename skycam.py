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
            self.comm = Communication(self, '0x50')
        else:
            self.comm = communication
        self.fapp = Flask(__name__)
        self.streamer = Streamer(self, cam)
        @self.fapp.route('/')
        def feed():
            return Response(self.streamer.stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
        self.th = FlaskThread(self.fapp)
        self.th.start()


if __name__ == '__main__':
    sk = Skycam()