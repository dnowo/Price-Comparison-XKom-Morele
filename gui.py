from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QLineEdit, QDesktopWidget
from PyQt5.QtCore import pyqtSlot

from shopscrapper import scrapFromXkom


class Gui(QWidget):

    def __init__(self):
        super().__init__()
        self.textboxCompareNameInput = QLineEdit()
        self.labelCompareNameInput = QLabel(self)

        self.labelComparedItem = QLabel(self)

        self.labelXkomShopName = QLabel(self)
        self.labelXkomItemPrice = QLabel(self)
        self.labelXkomItemAvailability = QLabel(self)

        self.labelMoreleShopName = QLabel(self)
        self.labelMoreleItemPrice = QLabel(self)
        self.labelMoreleItemAvailability = QLabel(self)

        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        # Input label, textbox, button
        self.labelCompareNameInput.setText("Wprowadź nazwę przedmiotu: ")
        self.labelCompareNameInput.adjustSize()
        self.labelComparedItem.adjustSize()

        self.textboxCompareNameInput.resize(100, 20)

        buttonCompareNameInput = QPushButton("Porównaj", self)
        buttonCompareNameInput.clicked.connect(self.runScraping)

        grid.addWidget(self.labelCompareNameInput, 1, 1)
        grid.addWidget(self.textboxCompareNameInput, 1, 2)
        grid.addWidget(buttonCompareNameInput, 1, 3)

        grid.addWidget(self.labelComparedItem, 2, 2)

        # Show diffrence
        self.labelXkomShopName.adjustSize()
        self.labelXkomItemPrice.adjustSize()
        self.labelXkomItemAvailability.adjustSize()

        grid.addWidget(self.labelXkomShopName, 3, 1)
        grid.addWidget(self.labelXkomItemPrice, 4, 1)
        grid.addWidget(self.labelXkomItemAvailability, 5, 1)

        self.labelMoreleShopName.adjustSize()
        self.labelMoreleItemPrice.adjustSize()
        self.labelMoreleItemAvailability.adjustSize()

        grid.addWidget(self.labelMoreleShopName, 3, 2)
        grid.addWidget(self.labelMoreleItemPrice, 4, 2)
        grid.addWidget(self.labelMoreleItemAvailability, 5, 2)

        # Show gui
        self.setLayout(grid)
        self.move(QDesktopWidget().availableGeometry().center())
        self.setWindowTitle("Porównaj ceny")
        self.show()

    @pyqtSlot()
    def runScraping(self):
        xKomProduct = scrapFromXkom(self.textboxCompareNameInput.text())
        # Item name label
        self.labelComparedItem.setText(str(xKomProduct.product_name))

        # Item from XKom.pl
        self.labelXkomShopName.setText(str(xKomProduct.shop_name))
        self.labelXkomItemPrice.setText(str(xKomProduct.product_price))
        self.labelXkomItemAvailability.setText(
            str("Dostępny" if xKomProduct.product_availability is True else "Niedostępny"))
