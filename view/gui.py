import urllib

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi

from service.shopscrapper import scrapFromXkom, scrapFromMorele
from view.vieweditor import productLinkFormat


def calculateDiffrence(xkom, morele):
    if xkom.product_price == "Brak danych" or morele.product_price == "Brak danych":
        return "Brak danych do porównania ceny"
    xkomPrice = float(xkom.product_price.replace("zł", "").replace(" ", "").replace(",", "."))
    morelePrice = float(morele.product_price.replace("zł", "").replace(" ", "").replace(",", "."))
    print("xkom")
    print(xkomPrice)
    print(xkomPrice)
    print(xkomPrice)
    print("Morele")
    print(morelePrice)
    print(morelePrice)
    print(morelePrice)
    if xkomPrice < morelePrice:
        return "Mniejszą cenę o " + str(round(float(morelePrice - xkomPrice), 2)) + " ma x-kom.pl"
    if morelePrice < xkomPrice:
        return "Mniejszą cenę o " + str(round(float(xkomPrice - morelePrice), 2)) + " ma Morele.net"
    if morelePrice == xkomPrice:
        return "Ceny są takie same :)"


class Gui(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi("./view/mainwindow.ui", self)
        self.setWindowTitle("Porównaj ceny w sklepach")
        # App icon
        app_icon = QIcon()
        app_icon.addFile('./assets/ico.png', QtCore.QSize(16, 16))

        self.setWindowIcon(app_icon)
        self.labelXkomItemLink.setOpenExternalLinks(True)
        self.labelMoreleItemLink.setOpenExternalLinks(True)
        self.hideLabelsMorele()
        self.hideLabelsXkom()
        self.hideSummary()

        self.buttonCheckPrice.clicked.connect(self.runScraping)
        self.move(QDesktopWidget().availableGeometry().center())

    @pyqtSlot()
    def runScraping(self):
        xKomProduct = scrapFromXkom(self.lineInputKeywords.text())
        moreleProduct = scrapFromMorele(self.lineInputKeywords.text())
        moreleProduct.product_image = xKomProduct.product_image
        errString = ["Nie mogę znaleźć przedmiotu w sklepie: "]
        self.labelDiffrence.show()
        if xKomProduct == 0 and moreleProduct == 0:
            self.labelError.setText(errString[0] + "Morele.net oraz x-kom.pl")
            self.hideLabelsXkom()
            self.hideLabelsMorele()
            self.labelImage.hide()
            return

        if xKomProduct == 0:
            self.labelError.setText(errString[0] + "x-kom.pl")
            self.labelMoreleComparedItem.setText(str(moreleProduct.product_name))
            self.labelMoreleShopName.setText(str(moreleProduct.shop_name))
            self.labelMoreleItemPrice.setText(str(moreleProduct.product_price))
            self.labelMoreleItemLink.setText(productLinkFormat(moreleProduct))
            self.labelMoreleItemAvailability.setText(
                str("Dostępny" if moreleProduct.product_availability is True else "Niedostępny"))
            self.hideLabelsXkom()
            return

        if moreleProduct == 0:
            self.labelError.setText(errString[0] + "Morele.net")
            self.labelXkomComparedItem.setText(str(xKomProduct.product_name))
            self.labelXkomShopName.setText(str(xKomProduct.shop_name))
            self.labelXkomItemPrice.setText(str(xKomProduct.product_price))
            self.labelXkomItemLink.setText(productLinkFormat(xKomProduct))
            self.labelXkomItemAvailability.setText(
                str("Dostępny" if xKomProduct.product_availability is True else "Niedostępny"))
            self.hideLabelsMorele()
            return

        self.labelError.show()
        self.labelError.setText("")
        self.showLabelsMorele()
        self.showLabelsXkom()
        self.labelImage.show()

        # Item from XKom.pl
        self.labelXkomComparedItem.setText(str(xKomProduct.product_name))
        self.labelXkomShopName.setText(str(xKomProduct.shop_name))
        self.labelXkomItemPrice.setText(str(xKomProduct.product_price))
        self.labelXkomItemLink.setText(productLinkFormat(xKomProduct))
        self.labelXkomItemAvailability.setText(
            str("Dostępny" if xKomProduct.product_availability is True else "Niedostępny"))

        # Item from Morele.net
        self.labelMoreleComparedItem.setText(str(moreleProduct.product_name))
        self.labelMoreleShopName.setText(str(moreleProduct.shop_name))
        self.labelMoreleItemPrice.setText(str(moreleProduct.product_price))
        self.labelMoreleItemLink.setText(productLinkFormat(moreleProduct))
        self.labelMoreleItemAvailability.setText(
            str("Dostępny" if moreleProduct.product_availability is True else "Niedostępny"))

        # Set image
        print(xKomProduct.product_image)
        if len(xKomProduct.product_image) > 1:
            data = urllib.request.urlopen(xKomProduct.product_image).read()
            image = QImage()
            image.loadFromData(data)
            self.labelImage.setPixmap(QPixmap(image))
            # .scaled(150, 150, QtCore.Qt.KeepAspectRatio)
        else:
            self.labelImage.setText("Brak zdjęcia")

        # Calc price diffrence
        self.labelDiffrence.show()
        self.labelDiffrence.setText(calculateDiffrence(xKomProduct, moreleProduct))

    def hideLabelsMorele(self):
        self.labelMoreleComparedItem.hide()
        self.labelMoreleShopName.hide()
        self.labelMoreleItemPrice.hide()
        self.labelMoreleItemAvailability.hide()
        self.labelMoreleItemLink.hide()

    def hideLabelsXkom(self):
        self.labelXkomComparedItem.hide()
        self.labelXkomShopName.hide()
        self.labelXkomItemPrice.hide()
        self.labelXkomItemLink.hide()
        self.labelXkomItemAvailability.hide()

    def hideSummary(self):
        self.labelError.hide()
        self.labelImage.hide()
        self.labelDiffrence.hide()

    def showLabelsXkom(self):
        self.labelXkomComparedItem.show()
        self.labelXkomShopName.show()
        self.labelXkomItemPrice.show()
        self.labelXkomItemLink.show()
        self.labelXkomItemAvailability.show()

    def showLabelsMorele(self):
        self.labelMoreleComparedItem.show()
        self.labelMoreleShopName.show()
        self.labelMoreleItemPrice.show()
        self.labelMoreleItemAvailability.show()
        self.labelMoreleItemLink.show()

    def showSummaryLabels(self):
        self.labelImage.show()
        self.labelDiffrence.show()
        self.labelError.show()