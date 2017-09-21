#!/usr/local/bin/python3.6

import sys
import argparse


parser = argparse.ArgumentParser(description="Skycam application")
parser.add_argument("-g", "--gui", action="store_true")
args = parser.parse_args()

def gui_main():
    from PyQt5.QtWidgets import QApplication
    from gui import MyMainWindow
    app = QApplication(sys.argv)
    window = MyMainWindow(app)
    sys.exit(app.exec_())

if __name__ == "__main__":
    if not args.gui:
        import web
        from skycam import Skycam
        from picamera import PiCamera
        cam = PiCamera()
        sk = Skycam(None, cam)
        web.main(sk)
    else:
        gui_main()
