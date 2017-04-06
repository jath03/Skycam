#!/usr/bin/python3.5

from PyQt5.QtCore import pyqtSignal, pyqtSlot
import sys

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QTabWidget, QApplication
from skycam import Skycam


class SkycamWidget(QWidget):
    def __init__(self, skycam=Skycam()):
        super().__init__()
        self.skycam = skycam

    def init_tabwidget(self):
        tw = QTabWidget(self)
        self.setCentralWidget(tw)
        self.sk = SkycamWidget()
        tw.show()



class MyMainWindow(QMainWindow):
    def __init__(self, widget=None, app=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.init_menubar()
        self.init_tabwidget()
        self.fs = False
        if widget is not None:
            self.setCentralWidget(widget)
        self.setGeometry(0, 0, 800, 600)
        self.move(self.app.desktop().screen().rect().center() - self.rect().center())
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





    @pyqtSlot()
    def exit(self):
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
    m = MyMainWindow(app=app)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
