from fastapi import APIRouter, HTTPException, Depends
from src.application.product_service import (
    CreateProduct,
    GetAllProducts,
    ProductRepository,
)
from src.domain.product import Product
from src.infrastructure.product_repository import SQLProductRepository
from typing import List

router = APIRouter(prefix="/products", tags=["products"])


def get_product_repository() -> ProductRepository:
    return SQLProductRepository()


@router.post("/", response_model=Product, status_code=201)
async def create_product(
    product: Product,
    repository: ProductRepository = Depends(get_product_repository),
):
    try:
        create_product_use_case = CreateProduct(repository)
        return create_product_use_case.execute(product)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=List[Product])
async def get_all_products(
    repository: ProductRepository = Depends(get_product_repository),
):
    try:
        get_all_products_use_case = GetAllProducts(repository)
        return get_all_products_use_case.execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")