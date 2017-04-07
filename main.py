#!/usr/bin/python3.5
import queue

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QUrl, QThread, QObject
import sys
from PyQt5.QtGui import QKeySequence, QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QTabWidget, QApplication, QBoxLayout, QHBoxLayout, \
    QVBoxLayout, QLabel
from skycam import Skycam
from streamer import StreamReciever


class SkycamWidget(QWidget):
    def __init__(self, skycam=Skycam(), streams=[]):
        super().__init__()
        self.skycam = skycam
        self.streams = dict()
        for i in range(len(streams)):
            self.streams[str(i)] = streams[i]
        print(self.streams)
        self.init_tabwidget()
        self.init_streams()
        self.init_layout()

    def init_layout(self):
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox.addLayout(vbox)
        hbox.addSpacing(1)
        hbox.addWidget(self.tw)
        self.setLayout(hbox)


    def init_tabwidget(self):
        self.tw = QTabWidget()

    def init_streams(self):
        for id, stream in self.streams.items():
            lb = QLabel()
            stream.id = id
            stream.lb = lb
            self.tw.addTab(stream.lb, 'Stream ' + id)
            th = QThread()
            stream.moveToThread(th)
            th.started.connect(stream.run)
            th.start()
            stream.newImage.connect(self.update_stream)

    @pyqtSlot(QImage, int)
    def update_stream(self, frame, id):
        pix = QPixmap.fromImage(frame)
        for id1, stream in self.streams:
            if id == id1:
                stream.lb.setPixmap(pix)



class MyMainWindow(QMainWindow):
    def __init__(self, widget=None, app=None, *args, **kwargs):
        print('initiating super')
        super().__init__(*args, **kwargs)
        self.app = app
        self.init_menubar()
        self.fs = False
        if widget is not None:
            self.setCentralWidget(widget)
        self.setGeometry(0, 0, 800, 600)
        self.move(self.app.desktop().screen().rect().center() - self.rect().center())
        self.w = widget
        self.w.skycam.streamer.errEvt.connect(self.pr)

        self.setCentralWidget(self.w)
        print('showing ...')
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

    @pyqtSlot(object)
    def pr(self, s):
        print(repr(s))





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
    w = SkycamWidget(streams=[StreamReciever('http://localhost:7777')])
    m = MyMainWindow(widget=w, app=app)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
