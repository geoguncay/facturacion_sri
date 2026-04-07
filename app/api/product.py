from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.database import models
from app.schemas import product_schema

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=product_schema.Product)
def create_product(product: product_schema.CreateProduct, db: Session = Depends(get_db)):
    """Create a new product."""
    new = models.Product(**product.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@router.get("/", response_model=list[product_schema.Product])
def list_products(db: Session = Depends(get_db)):
    """List all products."""
    products = db.query(models.Product).all()
    if not products:
        raise HTTPException(status_code=404, detail="No se encontraron productos. La lista está vacía.")
    return products