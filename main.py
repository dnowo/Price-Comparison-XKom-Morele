import sys

from PyQt5.QtWidgets import QApplication

from view import gui

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = gui.Gui()
    window.show()
    sys.exit(app.exec_())
