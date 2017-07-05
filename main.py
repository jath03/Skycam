#!/usr/local/bin/python3.6

import sys
import argparse


parser = argparse.ArgumentParser(description="Skycam application")
parser.add_argument("-w", "--web", action="store_true")
args = parser.parse_args()

def gui_main():
    from PyQt5.QtWidgets import QApplication
    from gui import MyMainWindow
    app = QApplication(sys.argv)
    window = MyMainWindow(app)
    sys.exit(app.exec_())

if __name__ == "__main__":
    if args.web:
        import web
        # from skycam import Skycam

        web.main()
    else:
        gui_main()
