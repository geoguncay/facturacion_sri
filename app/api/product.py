from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.database import models
from app.schemas import product_schema

router = APIRouter(
    prefix="/products",
    tags=["Productos"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_product(product: product_schema.CreateProduct, db: Session = Depends(get_db)):

    new = models.Product(**product.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@router.get("/")
def list_products(db: Session = Depends(get_db)):

    return db.query(models.Product).all()