# uncompyle6 version 2.9.10
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Nov 17 2016, 17:05:23) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jack/projects/local/testing/skycam/streamer.py
# Compiled at: 2017-04-04 16:20:50
# Size of source mod 2**32: 1160 bytes
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from flask import Flask, render_template, Response
import cv2
import json
fapp = Flask(__name__)

class Streamer(QThread):
    flipEvt = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cam = cv2.VideoCapture(0)
        self.flipped = False
        self.flipEvt.connect(self.flip)

    @fapp.route('/')
    def video_feed(self):
        return Response(self.stream(self.cam), mimetype='multipart/x-mixed-replace; boundary=frame')

    def stream(self, cam):
        while True:
            s, img = cam.read()
            cv2.imshow('Image', img)
            s, jpg = cv2.imencode('.jpg', img)
            cv2.imshow(jpg)
            frame = jpg.tobytes()
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'

    def run(self):
        fapp.run(host='localhost', port=7777, debug=True)

    def flip(self, evt=None):
        print('filpping', evt)
        self.flipped = not self.flipped
        print(self.flipped)