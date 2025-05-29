from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class Product(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)

    model_config = ConfigDict(from_attributes=True)