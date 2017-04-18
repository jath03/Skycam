import sys

import time
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QApplication
from flask import Flask, render_template, Response
import cv2
import json

fapp = Flask(__name__)
cam = cv2.VideoCapture(-1)
global flipped
flipped = False


class Streamer(QObject):
    flipEvt = pyqtSignal()
    errEvt = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flipEvt.connect(self.flip)

    def stream(self):
        while True:
            time.sleep(.05)
            s, img = cam.read()
            print('Camera working?', s)
            if not s:
                cam.release()
                continue
            if flipped:
                (h, w) = img.shape[:2]
                center = (w / 2, h / 2)
                M = cv2.getRotationMatrix2D(center, 180, 1.0)
                img = cv2.warpAffine(img, M, (w, h))
            s, jpg = cv2.imencode('.jpg', img)
            frame = jpg.tobytes()
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'


    @pyqtSlot()
    def flip(self):
        print('filpping')
        global flipped
        flipped = not flipped
        print(self.flipped)


class StreamReciever(QObject):
    newImage = pyqtSignal(QImage, int)
    def __init__(self, address):
        super().__init__()
        self.address = address

    def run(self):
        cap = cv2.VideoCapture(self.address)
        while cap.isOpened():
            _, frame = cap.read()
            image = QImage(frame.tostring(), 640, 480, QImage.Format_RGB888).rgbSwapped()
            self.newImage.emit(image, self.id)


@fapp.route('/')
def video_feed():
    return Response(st.stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

def main(streamer):
    try:
        global st
        st = streamer
        fapp.run(host='localhost', port=7777, debug=True)
    except:
        cam.release()
        raise

if __name__ == '__main__':
    s = Streamer()
    main(s)