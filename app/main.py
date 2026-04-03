from fastapi import FastAPI
from app.database.db import engine
from app.database import models
from app.api import client, invoice, product

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Facturación SRI")

app.include_router(client.router)
app.include_router(invoice.router)
app.include_router(product.router)



@app.get("/")
def root():
    return {"message": "Sistema de Facturación SRI"}