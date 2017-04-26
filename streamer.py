import sys

import time
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject, QCoreApplication
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QApplication
from flask import Flask, render_template, Response
import cv2
import json


class Streamer(QObject):
    flipEvt = pyqtSignal()
    errEvt = pyqtSignal(object)

    def __init__(self, master, cam, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flipEvt.connect(self.flip)
        self.cam = cam
        self.flipped = False

    def stream(self):
        while True:
            QCoreApplication.processEvents()
            time.sleep(.05)
            s, img = self.cam.read()
            print('Camera working?', s)
            if not s:
                self.cam.release()
                continue
            if self.flipped:
                (h, w) = img.shape[:2]
                center = (w / 2, h / 2)
                M = cv2.getRotationMatrix2D(center, 180, 1.0)
                img = cv2.warpAffine(img, M, (w, h))
            s, jpg = cv2.imencode('.jpg', img)
            frame = jpg.tobytes()
            yield b'--frame\r\nContent-Type: image/jpeg\r\nContent-Length:' + bytes(len(frame)) + b'\r\n\r\n' + frame + b'\r\n\r\n'


    @pyqtSlot()
    def flip(self):
        print('filpping')
        self.flipped = not self.flipped
        print(self.flipped)


class StreamReciever(QObject):
    newImage = pyqtSignal(QImage, str)
    def __init__(self, master, address):
        super().__init__()
        self.address = address

    def run(self):
        cap = cv2.VideoCapture(self.address)
        while cap.isOpened():
            i, frame = cap.read()
            if i:
                image = QImage(frame.tostring(), 640, 480, QImage.Format_RGB888).rgbSwapped()
                self.newImage.emit(image, self.id)


class FlaskThread(QThread):
    def __init__(self, application):
        super().__init__()
        self.application = application

    def __del__(self):
        self.wait()

    def run(self):
        self.application.run(host='localhost', port=7777, debug=False, use_reloader=False)


def main(fapp, cam):
    try:
        fapp.run(host='localhost', port=7777, debug=False, use_reloader=False)
    except:
        cam.release()
        raise

if __name__ == '__main__':
    s = Streamer()
    main(s)