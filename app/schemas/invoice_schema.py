from pydantic import BaseModel
from typing import List


class CreateInvoiceDetail(BaseModel):

    product: str
    quantity: int
    price: float


class CreateInvoice(BaseModel):

    client_id: int
    details: List[CreateInvoiceDetail]