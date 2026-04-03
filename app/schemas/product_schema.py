from pydantic import BaseModel


class CreateProduct(BaseModel):

    product_name: str
    price: float
    iva: float


class Product(CreateProduct):

    id: int

    class Config:
        orm_mode = True