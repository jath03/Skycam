import sys
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication
from flask import Flask, render_template, Response
import cv2
import json

fapp = Flask(__name__)


class Streamer(QThread):
    flipEvt = pyqtSignal(object)

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
            if self.flipped:
                (h, w) = img.shape[:2]
                center = (w / 2, h / 2)
                M = cv2.getRotationMatrix2D(center, 180, 1.0)
                img = cv2.warpAffine(img, M, (w, h))
            s, jpg = cv2.imencode('.jpg', img)
            frame = jpg.tobytes()
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'

    def run(self):
        fapp.run(host='localhost', port=7777, debug=True)

    @pyqtSlot(object)
    def flip(self, evt=None):
        print('filpping', evt)
        self.flipped = not self.flipped
        print(self.flipped)