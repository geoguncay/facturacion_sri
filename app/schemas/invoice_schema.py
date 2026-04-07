from pydantic import BaseModel
from typing import List, Optional


class CreateInvoiceDetail(BaseModel):

    product: str
    quantity: int
    price: float


class InvoiceDetail(CreateInvoiceDetail):
    
    id: int
    invoice_id: int
    subtotal: float = 0.0

    class Config:
        from_attributes = True


class CreateInvoice(BaseModel):

    client_id: int
    details: List[CreateInvoiceDetail]


class Invoice(BaseModel):
    
    id: int
    client_id: int
    total: float
    state: str = "PENDING"
    details: Optional[List[InvoiceDetail]] = None

    class Config:
        from_attributes = True
