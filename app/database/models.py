import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database.db import Base

class Client(Base):

    __tablename__ = "client"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    identification = Column(String)
    address = Column(String)
    email = Column(String)
    invoices = relationship("Invoice", back_populates="client")

class Product(Base):

    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name_product = Column(String)
    price = Column(Float)
    iva = Column(Float)


class Invoice(Base):

    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("client.id"))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    total = Column(Float)
    state = Column(String, default="PENDIENTE")
    client = relationship("Client", back_populates="invoices")
    details = relationship("InvoiceDetail", back_populates="invoice")


class InvoiceDetail(Base):

    __tablename__ = "invoice_details"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    product = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
    subtotal = Column(Float)

    invoice = relationship("Invoice", back_populates="details")