#!/usr/bin/python3.5

import sys
from PyQt5.QtWidgets import QApplication
from tools import StdoutFilter, StderrFilter
from gui import MyMainWindow



def main():
    sys.stdout = StdoutFilter()
    sys.stderr = StderrFilter()
    app = QApplication(sys.argv)
    window = MyMainWindow(app)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
