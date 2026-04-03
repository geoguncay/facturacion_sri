from app.database import models
from app.sri.acces_key import generate_access_key
from app.sri.xml_generator import generate_invoice_xml


def calculate_total(details):

    total = 0

    for d in details:

        subtotal = d["quantity"] * d["price"]
        total += subtotal

    return total

def generate_invoice(invoice, client, details):

    key = generate_access_key(
        ruc="1790012345001",
        estab="001",
        pto_emision="001",
        secuencial=str(invoice.id).zfill(9)
    )

    data = {
        "razon_social": "MI EMPRESA ISP",
        "ruc": "1790012345001",
        "clave_acceso": key,
        "estab": "001",
        "pto_emision": "001",
        "secuencial": str(invoice.id).zfill(9),
        "fecha": invoice.fecha.strftime("%d/%m/%Y"),
        "direccion": client.direccion,
        "subtotal": invoice.total,
        "total": invoice.total,
        "details": details
    }

    return generate_invoice_xml(data)