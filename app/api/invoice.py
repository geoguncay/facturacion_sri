from fastapi import APIRouter, Depends, HTTPException
from app.database.db import SessionLocal
from app.services.service_invoice import calculate_total
from app.schemas import invoice_schema
from sqlalchemy.orm import Session
from app.database import models

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=invoice_schema.Invoice)
def create_invoice(data: invoice_schema.CreateInvoice, db: Session = Depends(get_db)):
    """Create a new invoice with details."""
    
    # Calculate total from details
    total = calculate_total([d.dict() for d in data.details])

    # Create invoice
    invoice = models.Invoice(
        client_id=data.client_id,
        total=total
    )   

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    # Create invoice details
    for d in data.details:
        subtotal = d.quantity * d.price
        detail = models.InvoiceDetail(
            invoice_id=invoice.id,
            product=d.product,
            quantity=d.quantity,
            price=d.price,
            subtotal=subtotal
        )
        db.add(detail)
    
    db.commit()
    
    # Refresh to load relationships
    db.refresh(invoice)
    
    return invoice

@router.get("/", response_model=list[invoice_schema.Invoice])
def list_invoices(db: Session = Depends(get_db)):
    """List all invoices."""
    invoices = db.query(models.Invoice).all()
    if not invoices:
        raise HTTPException(status_code=404, detail="No se encontraron facturas. La lista está vacía.")
    return invoices

