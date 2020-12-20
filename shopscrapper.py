from functools import reduce

import requests
from bs4 import BeautifulSoup
from urllib import request

from Item import Item

xKomUrl = "https://www.x-kom.pl/"
moreleUrl = "https://www.morele.net/"


def responseXkom(url: str):
    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def responseMorele(url: str):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup


def scrapFromXkom(productQuery: str):
    url = xKomUrl + "szukaj?q=" + productQuery.replace(" ", "%20")
    soup = responseXkom(url)
    aResults = soup.find_all("a", class_="sc-1h16fat-0 sc-1yu46qn-10 dFAarG", href=True)
    for a in aResults:
        print(a["href"])
    if len(aResults) < 1:
        print("Nie znaleziono przedmiotu!")
        return 0
    productUrl = xKomUrl + aResults[0]["href"]
    print(productUrl)
    soupProduct = responseXkom(productUrl)
    productAvailable = False
    if soupProduct.find("span", class_="sc-1hdxfw1-1 cMQxDU") is not None:
        productAvailable = True
    return Item("x-kom",
                soupProduct.find("h1", class_="sc-1x6crnh-5").text if soupProduct.find("h1", class_="sc-1x6crnh-5") is not None else "Brak danych",
                soupProduct.find("div", class_="u7xnnm-4 iVazGO").text if soupProduct.find("div", class_="u7xnnm-4 iVazGO") is not None else "Brak danych",
                productAvailable)


def scrapFromMorele(productQuery: str):
    url = moreleUrl + "wyszukiwarka/0/0/,,,,,,,,,,,,/1/?q=" + productQuery.replace(" ", "+")
    soup = responseMorele(url)
    aResults = soup.find_all("a", class_="productLink", href=True)
    for a in aResults:
        print(a["href"])
    if len(aResults) < 1:
        print("Nie znaleziono przedmiotu!")
        return 0

    productUrl = moreleUrl + str(aResults[0]["href"]).replace("/", "", 1)
    print(productUrl)

    soupProduct = responseMorele(productUrl)
    productAvailable = True
    if soupProduct.find("div", class_="prod-available-items") is None:
        productAvailableString = "0"
    else:
        productAvailableString = soupProduct.find("div", class_="prod-available-items").text

    for r in (("Dostępnych", ""), ("szt.", ""), (" ", ""), ("Zostało", ""), ("tylko", "")):
        productAvailableString = productAvailableString.replace(*r)
    if productAvailableString is None or int(productAvailableString) < 1:
        productAvailable = False
    return Item("Morele.net",
                soupProduct.find("h1", class_="prod-name").text if soupProduct.find("h1", class_="prod-name") is not None else "Brak danych",
                soupProduct.find_all("div", class_="product-price")[0]["data-default"] if soupProduct.find_all("div", class_="product-price")[0]["data-default"] is not None else "Brak danych",
                productAvailable)

