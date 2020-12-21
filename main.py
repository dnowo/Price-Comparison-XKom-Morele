import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow

import gui


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Porównaj ceny w sklepach")
        self.setCentralWidget(gui.Gui())
        # App icon
        app_icon = QtGui.QIcon()
        app_icon.addFile('ico.png', QtCore.QSize(16, 16))
        app_icon.addFile('ico.png', QtCore.QSize(24, 24))
        app_icon.addFile('ico.png', QtCore.QSize(32, 32))
        app_icon.addFile('ico.png', QtCore.QSize(48, 48))
        app_icon.addFile('ico.png', QtCore.QSize(256, 256))
        self.setWindowIcon(app_icon)


stylesheet = """
                MainWindow {
                    background-image: url("bg.png"); 
                    background-repeat: repeat-x; 
                }
             """

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
