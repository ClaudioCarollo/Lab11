from dataclasses import dataclass

from model.product import Go_product


@dataclass
class Connessione:
    product1: Go_product
    product2: Go_product
    peso: int
