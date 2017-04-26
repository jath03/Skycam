#!/usr/bin/python3.5
import queue
from PyQt5 import QtCore

import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QUrl, QThread, QObject
import sys
from PyQt5.QtGui import QKeySequence, QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QTabWidget, QApplication, QBoxLayout, QHBoxLayout, \
    QVBoxLayout, QLabel, QGridLayout, QScrollArea, QListWidget
from flask import Flask, Response
from skycam import Skycam
from streamer import StreamReciever
from tools import StdoutFilter, StderrFilter


class SkycamWidget(QWidget):
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
        hbox.addWidget(self.tw)
        hbox.addLayout(vbox)
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
        pix = pix.scaledToHeight(self.frameGeometry().height() - 150)
        for id1, stream in self.streams.items():
            if id == id1:
                stream.lb.setPixmap(pix)



class MyMainWindow(QMainWindow):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_menubar()
        self.app = app
        self.fs = False
        self.settings = None
        self.cam = cv2.VideoCapture(0)
        self.setGeometry(0, 0, 800, 600)
        self.move(self.app.desktop().screen().rect().center() - self.rect().center())
        print('showing ...')
        self.st = [StreamReciever(self, 'http://localhost:7777')]
        self.w = SkycamWidget(self, self.cam, self.st)
        self.setWindowTitle('Skycam')
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
        settings = QAction("Settings", self)
        settings.setShortcut(QKeySequence('Ctrl+S'))
        settings.setStatusTip('Open settings menu')
        settings.triggered.connect(self.open_settings)


        view = self.bar.addMenu("View")

        file.addAction(settings)
        file.addAction(quit)
        view.addAction(fullscreen)

    @pyqtSlot(object)
    def pr(self, s):
        print(repr(s))


    @pyqtSlot()
    def exit(self):
        self.cam.release()
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

    @pyqtSlot()
    def open_settings(self):
        if self.settings:
            self.settings.setWindowState(
                self.settings.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
            self.settings.activateWindow()
        else:
            self.settings = Settings()
            self.settings.setWindowState(
                self.settings.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
            self.settings.activateWindow()

    @pyqtSlot()
    def settings_closed(self):
        self.settings = None


class Settings(QWidget):
    closed = pyqtSignal()

    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master = master
        self.setWindowTitle('Settings')
        self.closed.connect(master.settings_closed)
        self.show()

    def init_layout(self):
        grid = QGridLayout()


        listw = QListWidget()
        for stream in self.master.st:
            listw.addItem('Stream ' + stream.address)
        scroll = QScrollArea()
        scroll.setWidget(listw)

        grid.addWidget(scroll)

        self.setLayout(grid)

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()


def settings_main():
    app = QApplication(sys.argv)
    settings = Settings()
    sys.exit(app.exec_())

if __name__ == '__main__':
    settings_main()