from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.database import models
from app.schemas import client_schema


router = APIRouter(
    prefix="/clients",
    tags=["Clientes"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_client(client: client_schema.CreateClient, db: Session = Depends(get_db)):

    new = models.Client(**client.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@router.get("/")
def list_clients(db: Session = Depends(get_db)):

    return db.query(models.Client).all()