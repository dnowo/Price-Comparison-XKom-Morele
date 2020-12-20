from bs4 import BeautifulSoup
import requests
from urllib import request

from Item import Item

xKomUrl = "https://www.x-kom.pl/"


def response(url: str):
    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def scrapFromXkom(productQuery: str):
    url = xKomUrl + "szukaj?q=" + productQuery.replace(" ", "%20")
    soup = response(url)
    aResults = soup.find_all("a", class_="sc-1h16fat-0 sc-1yu46qn-10 dFAarG", href=True)
    for a in aResults:
        print(a["href"])
    if len(aResults) < 1:
        print("Nie znaleziono przedmiotu!")
        return None
    productUrl = xKomUrl + aResults[0]["href"]
    print(productUrl)
    soupProduct = response(productUrl)
    productAvailable = False
    if soupProduct.find("span", class_="sc-1hdxfw1-1 cMQxDU") is not None:
        productAvailable = True
    product = Item("x-kom", soupProduct.find("h1", class_="sc-1x6crnh-5").text, soupProduct.find("div", class_="u7xnnm-4 iVazGO").text, productAvailable)
    return product
