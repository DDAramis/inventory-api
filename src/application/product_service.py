from abc import ABC, abstractmethod
from typing import List
from src.domain.product import Product

class ProductRepository(ABC):
    def create(self, prorduct: Product) -> Product:
        pass

    @abstractmethod
    def get_all(self) -> List[Product]:
        pass

class CreateProduct:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, product: Product) -> Product:

        if product.price <= 0:
            raise ValueError("Price must be greater than zero.")
        if product.stock < 0:
            raise ValueError("Stock cannot be negative.")
        return self.repository.create(product)
    
class GetAllProducts:
    def __init__(self, repository: ProductRepository):
        self.repository = repository
    def execute(self) -> List[Product]:
        return self.repository.get_all()