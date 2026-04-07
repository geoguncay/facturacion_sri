from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.database import models
from app.schemas import client_schema


router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=client_schema.Client)
def create_client(client: client_schema.CreateClient, db: Session = Depends(get_db)):
    """Create a new client."""
    new = models.Client(**client.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@router.get("/", response_model=list[client_schema.Client])
def list_clients(db: Session = Depends(get_db)):
    """List all clients."""
    clients = db.query(models.Client).all()
    if not clients:
        raise HTTPException(status_code=404, detail="No se encontraron clientes. La lista está vacía.")
    return clients