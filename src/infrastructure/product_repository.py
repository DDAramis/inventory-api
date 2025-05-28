from typing import List
from src.application.product_service import ProductRepository
from src.domain.product import Product
from src.infrastructure.database import ProductDB, get_db
from sqlalchemy.orm import Session


class SQLProductRepository(ProductRepository):
    def __Init__(self):
        pass
    
    def create(self, product: Product) -> Product:
        db: Session = next(get_db)
        try:
            db_product = ProductDB(
                name=product.name,
                price=product.price,
                stock=product.stock
            )
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            product.id = db_product.id
            return product
        finally:
            db.close()

    def get_all(self) -> List[Product]:
        db: Session = next(get_db)
        try:
            db_products = db.query(ProductDB).all()
            return [Product(**product.__dict__) for product in db_products]
        finally:
            db.close()