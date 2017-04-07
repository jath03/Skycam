#!/usr/bin/python3.5
from PyQt5.QtCore import QObject, QThread
from communication import Communication
from streamer import Streamer


class Skycam(QObject):
    def __init__(self, communication=None):
        super().__init__()
        if not communication:
            self.comm = Communication('0x50')
        else:
            self.comm = communication
        self.streamer = Streamer()
        th = QThread()
        self.streamer.moveToThread(th)
        th.started.connect(self.streamer.run)
        th.start()


if __name__ == '__main__':
    sk = Skycam()