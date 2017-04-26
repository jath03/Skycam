#!/usr/bin/python3.5
import queue

import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QUrl, QThread, QObject
import sys
from PyQt5.QtGui import QKeySequence, QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QTabWidget, QApplication, QBoxLayout, QHBoxLayout, \
    QVBoxLayout, QLabel
from flask import Flask, Response
from skycam import Skycam
from streamer import StreamReciever


class SkycamWidget(QWidget):
    resizePic = pyqtSignal(int, int)
    def __init__(self, master, cam, streams=[]):
        print('initiating skycam widget')
        super().__init__()
        self.skycam = Skycam(self, cam)
        self.master = master
        self.master.setCentralWidget(self)
        self.streams = dict()
        self.th = list()
        for i in range(len(streams)):
            self.streams[str(i)] = streams[i]
        print(self.streams)
        self.init_tabwidget()
        self.init_streams()
        self.init_layout()
        print('initiated skycam widget')


    def init_layout(self):
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox.addLayout(vbox)
        hbox.addWidget(self.tw)
        self.setLayout(hbox)


    def init_tabwidget(self):
        self.tw = QTabWidget()

    def init_streams(self):
        for id, stream in self.streams.items():
            print('initiating stream', id)
            lb = QLabel()
            stream.id = id
            stream.lb = lb
            self.tw.addTab(stream.lb, 'Stream ' + id)
            th = QThread()
            stream.moveToThread(th)
            th.started.connect(stream.run)
            self.th.append(th)
            th.start()
            stream.newImage.connect(self.update_stream)

    @pyqtSlot(QImage, str)
    def update_stream(self, frame, id):
        pix = QPixmap.fromImage(frame)
        for id1, stream in self.streams.items():
            if id == id1:
                stream.lb.setPixmap(pix)



class MyMainWindow(QMainWindow):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_menubar()
        self.app = app
        self.fs = False
        self.cam = cv2.VideoCapture(0)
        self.setGeometry(0, 0, 800, 600)
        self.move(self.app.desktop().screen().rect().center() - self.rect().center())
        print('showing ...')
        st = [StreamReciever(self, 'http://localhost:7777')]
        self.w = SkycamWidget(self, self.cam, st)
        self.w.resizeEvent = self.img_resize
        self.show()



    def init_menubar(self):
        self.bar = self.menuBar()
        file = self.bar.addMenu("File")
        fullscreen = QAction("Fullsceen", self, checkable=True)
        fullscreen.setShortcut(QKeySequence('Ctrl+F'))
        fullscreen.setStatusTip("Toggle fullscreen")
        fullscreen.triggered.connect(self.fullscreen)
        quit = QAction("Quit", self)
        quit.setShortcut(QKeySequence('Ctrl+Q'))
        quit.setStatusTip('Quit Application')
        quit.triggered.connect(self.exit)
        view = self.bar.addMenu("View")

        file.addAction(quit)
        view.addAction(fullscreen)
        self.show()

    @pyqtSlot(object)
    def pr(self, s):
        print(repr(s))


    @pyqtSlot(object)
    def img_resize(self, event):
        print(event)


    @pyqtSlot()
    def exit(self):
        self.w.skycam.streamer.cam.release()
        self.app.quit()
        sys.exit()

    @pyqtSlot()
    def fullscreen(self):
        if self.fs == False:
            self.showFullScreen()
            self.fs = True
        else:
            self.showNormal()
            self.fs = False


def main():
    app = QApplication(sys.argv)
    window = MyMainWindow(app)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
