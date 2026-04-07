from app.database import models
from app.sri.access_key import generate_access_key
from app.sri.xml_generator import generate_invoice_xml
from app.sri.xml_signer import sign_xml
from app.sri.sri_client import SRIClient

def calculate_total(details):
    """Calculate the total from invoice details."""
    total = 0
    for d in details:
        subtotal = d["quantity"] * d["price"]
        total += subtotal
    return total

def generate_invoice(invoice, client, details):
    """Generate XML for an invoice."""
    key = generate_access_key(
        ruc="1790012345001",
        establishment="001",
        emission_point="001",
        sequential=str(invoice.id).zfill(9)
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

def send_invoice_to_sri(xml_path, p12_path, password, access_key):
    """Send signed invoice to SRI."""
    # Sign the XML
    signed_xml = sign_xml(xml_path, p12_path, password)

    # Send to SRI
    sri_client = SRIClient()
    response = sri_client.send_invoice(signed_xml)
    if response.state != "RECIBIDA":
        authorization_response = sri_client.consult_authorization(access_key)
        return authorization_response

    return response

