from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QLineEdit, QDesktopWidget
from PyQt5.QtCore import pyqtSlot

from PyQt5 import QtWidgets
from scrapy.crawler import CrawlerProcess

import shopscrapper


class Gui(QWidget):

    def __init__(self):
        super().__init__()
        self.textboxCompareNameInput = QLineEdit()
        self.labelCompareNameInput = QLabel()
        self.labelComparedItem = QLabel(self)
        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        # Input label, textbox, button
        self.labelCompareNameInput.setText("Wprowadź nazwę przedmiotu: ")
        self.labelCompareNameInput.adjustSize()

        self.textboxCompareNameInput.resize(100, 20)

        buttonCompareNameInput = QPushButton("Porównaj", self)
        buttonCompareNameInput.clicked.connect(self.runSpider)

        grid.addWidget(self.labelCompareNameInput, 1, 1)
        grid.addWidget(self.textboxCompareNameInput, 1, 2)
        grid.addWidget(buttonCompareNameInput, 1, 3)

        # Show diffrence
        self.labelComparedItem.adjustSize()

        grid.addWidget(self.labelComparedItem, 2, 1)

        # Show gui
        self.setLayout(grid)
        self.move(QDesktopWidget().availableGeometry().center())
        self.setWindowTitle("Porównaj ceny")
        self.show()

    @pyqtSlot()
    def runSpider(self):
        self.labelComparedItem.setText(str(self.textboxCompareNameInput.text()))
        # process = CrawlerProcess({
        #     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        # })
        #
        # process.crawl(shopscrapper.ShopsSpider)
        # process.start()

