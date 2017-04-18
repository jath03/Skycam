#!/usr/bin/python3.5
from PyQt5.QtCore import QObject, QThread
from communication import Communication
from streamer import Streamer, main
from functools import partial


class Skycam(QObject):
    def __init__(self, communication=None):
        super().__init__()
        if not communication:
            self.comm = Communication('0x50')
        else:
            self.comm = communication
        self.streamer = Streamer()
        self.th = QThread()
        self.streamer.moveToThread(self.th)
        self.th.started.connect(partial(main, self.streamer))
        self.th.start()


if __name__ == '__main__':
    sk = Skycam()