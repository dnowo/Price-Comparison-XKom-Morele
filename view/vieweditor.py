from model import Item


def productLinkFormat(product: Item) -> str:
    formatted = "<a href=\"" + product.product_link + "\">" + "Strona przedmiotu" + "</a>"
    return str(formatted)
