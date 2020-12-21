from dataclasses import dataclass


@dataclass
class Item:
    shop_name: str
    product_name: str
    product_price: str
    product_availability: bool
    product_link: str
