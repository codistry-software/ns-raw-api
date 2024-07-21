# src/webshops/dto/product_dto.py
from dataclasses import dataclass
from typing import Dict

@dataclass
class ProductDTO:
    name: str
    description: str
    price: float
    availability: bool
    category: str
    sale: bool
    ingredients: str
    nutritional_info: Dict[str, any]
