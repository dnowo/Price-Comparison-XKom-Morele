from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QLineEdit, QDesktopWidget
from PyQt5.QtCore import pyqtSlot

from shopscrapper import scrapFromXkom, scrapFromMorele


def calculateDiffrence(xkom, morele):
    if xkom.product_price == "Brak danych" or morele.product_price == "Brak danych":
        return "Brak danych do porównania ceny"
    xkomPrice = float(xkom.product_price.replace("zł", "").replace(" ", "").replace(",", "."))
    morelePrice = float(morele.product_price.replace("zł", "").replace(" ", "").replace(",", "."))
    if xkomPrice < morelePrice:
        return "Mniejszą cenę o " + str(round(float(morelePrice - xkomPrice), 2)) + " ma x-kom.pl"
    if morelePrice < xkomPrice:
        return "Mniejszą cenę o " + str(round(float(xkomPrice - morelePrice), 2)) + " ma Morele.net"


class Gui(QWidget):

    def __init__(self):
        super().__init__()
        self.textboxCompareNameInput = QLineEdit()
        self.labelCompareNameInput = QLabel(self)

        self.labelXkomComparedItem = QLabel(self)
        self.labelMoreleComparedItem = QLabel(self)

        self.labelXkomShopName = QLabel(self)
        self.labelXkomItemPrice = QLabel(self)
        self.labelXkomItemAvailability = QLabel(self)

        self.labelMoreleShopName = QLabel(self)
        self.labelMoreleItemPrice = QLabel(self)
        self.labelMoreleItemAvailability = QLabel(self)

        self.labelError = QLabel(self)

        self.labelDiffrence = QLabel(self)

        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        # Input label, textbox, button
        self.labelCompareNameInput.setText("Wprowadź słowa kluczowe przedmiotu: ")
        self.labelCompareNameInput.adjustSize()

        self.textboxCompareNameInput.adjustSize()

        buttonCompareNameInput = QPushButton("Porównaj", self)
        buttonCompareNameInput.clicked.connect(self.runScraping)

        grid.addWidget(self.labelCompareNameInput, 1, 1)
        grid.addWidget(self.textboxCompareNameInput, 1, 2, 1, 2)
        grid.addWidget(buttonCompareNameInput, 1, 4)

        self.labelError.adjustSize()
        grid.addWidget(self.labelError, 2, 2)

        self.labelDiffrence.adjustSize()
        grid.addWidget(self.labelDiffrence, 7, 2)

        # Show diffrence
        self.labelXkomShopName.adjustSize()
        self.labelXkomItemPrice.adjustSize()
        self.labelXkomItemAvailability.adjustSize()
        self.labelXkomComparedItem.adjustSize()

        grid.addWidget(self.labelXkomShopName, 3, 1)
        grid.addWidget(self.labelXkomComparedItem, 4, 1)
        grid.addWidget(self.labelXkomItemPrice, 5, 1)
        grid.addWidget(self.labelXkomItemAvailability, 6, 1)

        self.labelMoreleShopName.adjustSize()
        self.labelMoreleItemPrice.adjustSize()
        self.labelMoreleItemAvailability.adjustSize()
        self.labelMoreleComparedItem.adjustSize()

        grid.addWidget(self.labelMoreleShopName, 3, 3)
        grid.addWidget(self.labelMoreleComparedItem, 4, 3)
        grid.addWidget(self.labelMoreleItemPrice, 5, 3)
        grid.addWidget(self.labelMoreleItemAvailability, 6, 3)

        # Show gui
        self.setLayout(grid)
        self.move(QDesktopWidget().availableGeometry().center())
        self.setWindowTitle("Porównaj ceny w sklepach")
        self.show()

    @pyqtSlot()
    def runScraping(self):
        xKomProduct = scrapFromXkom(self.textboxCompareNameInput.text())
        moreleProduct = scrapFromMorele(self.textboxCompareNameInput.text())

        errString = ["Nie mogę znaleźć przedmiotu w sklepie: "]
        if xKomProduct == 0 and moreleProduct == 0:
            self.labelError.setText(errString[0] + "Morele.net oraz x-kom.pl")
            self.labelXkomComparedItem.setText("")
            self.labelXkomShopName.setText("")
            self.labelXkomItemPrice.setText("")
            self.labelXkomItemAvailability.setText("")
            self.labelMoreleComparedItem.setText("")
            self.labelMoreleShopName.setText("")
            self.labelMoreleItemPrice.setText("")
            self.labelMoreleItemAvailability.setText("")
            return

        if xKomProduct == 0:
            self.labelError.setText(errString[0] + "x-kom.pl")
            self.labelMoreleComparedItem.setText(str(moreleProduct.product_name))
            self.labelMoreleShopName.setText(str(moreleProduct.shop_name))
            self.labelMoreleItemPrice.setText(str(moreleProduct.product_price))
            self.labelMoreleItemAvailability.setText(
                str("Dostępny" if moreleProduct.product_availability is True else "Niedostępny"))
            self.labelXkomComparedItem.setText("")
            self.labelXkomShopName.setText("")
            self.labelXkomItemPrice.setText("")
            self.labelXkomItemAvailability.setText("")
            return

        if moreleProduct == 0:
            self.labelError.setText(errString[0] + "Morele.net")
            self.labelXkomComparedItem.setText(str(xKomProduct.product_name))
            self.labelXkomShopName.setText(str(xKomProduct.shop_name))
            self.labelXkomItemPrice.setText(str(xKomProduct.product_price))
            self.labelXkomItemAvailability.setText(
                str("Dostępny" if xKomProduct.product_availability is True else "Niedostępny"))
            self.labelMoreleComparedItem.setText("")
            self.labelMoreleShopName.setText("")
            self.labelMoreleItemPrice.setText("")
            self.labelMoreleItemAvailability.setText("")
            return

        self.labelError.setText("")

        # Item from XKom.pl
        self.labelXkomComparedItem.setText(str(xKomProduct.product_name))
        self.labelXkomShopName.setText(str(xKomProduct.shop_name))
        self.labelXkomItemPrice.setText(str(xKomProduct.product_price))
        self.labelXkomItemAvailability.setText(
            str("Dostępny" if xKomProduct.product_availability is True else "Niedostępny"))

        # Item from Morele.net
        self.labelMoreleComparedItem.setText(str(moreleProduct.product_name))
        self.labelMoreleShopName.setText(str(moreleProduct.shop_name))
        self.labelMoreleItemPrice.setText(str(moreleProduct.product_price))
        self.labelMoreleItemAvailability.setText(
            str("Dostępny" if moreleProduct.product_availability is True else "Niedostępny"))

        # Calc price diffrence
        self.labelDiffrence.setText(calculateDiffrence(xKomProduct, moreleProduct))
