import smbus
import time

class Communication(object):

    def __init__(self, master, address):
        self.address = address
        self.master = master
        self.bus = smbus.SMBus(1)
    def write(self, msg):
        for char in str(msg):
            self.bus.write_byte(self.address, ord(char))
        self.bus.write_byte(self.address, ord('\n'))
    def read(self):
        bytes_lst = []
        while True:
            time.sleep(.2)
            b = self.bus.read_byte(self.address)
            if b != ord('\n'):
                bytes_lst.append(b)
            else:
                st = ''.join([chr(byte) for byte in bytes_lst])
                return st
    def write_byte(self, num):
        self.bus.write_byte(self.address, ord(char))
    def read_byte(self):
        return self.bus.read_byte(self.address)
