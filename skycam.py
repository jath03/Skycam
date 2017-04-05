#!/usr/bin/python3.5

from communication import Communication
from streamer import Streamer

class Skycam(QObject):
    def __init__(self, communication=None):
        if not communication:
            self.comm = Communication('0x50')
        else:
            self.comm = communication
        self.streamer = Streamer()


if __name__ == '__main__':
    sk = Skycam()