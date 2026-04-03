from fastapi import APIRouter, Depends
from app.database.db import SessionLocal
from app.services.service_invoice import calculate_total
from app.schemas import invoice_schema
from sqlalchemy.orm import Session
from app.database import models

router = APIRouter(
    prefix="/invoices",
    tags=["Facturas"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_invoice(data: invoice_schema.CreateInvoice, db: Session = Depends(get_db)):

    total = calculate_total([d.dict() for d in data.detalles])

    invoice = models.Invoice(
        client_id=data.client_id,
        total=total
    )   

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    for d in data.detalles:
        detail = models.InvoiceDetail(
            invoice_id=invoice.id,
            product_id=d.product_id,
            quantity=d.quantity,
            price=d.price
        )
        db.add(detail)
    db.commit()
    return invoice

@router.get("/")
def list_invoices(db: Session = Depends(get_db)):
    return db.query(models.Invoice).all()

