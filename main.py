import sys

from PyQt5.QtWidgets import QApplication

import gui


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = gui.Gui()
    sys.exit(app.exec_())
