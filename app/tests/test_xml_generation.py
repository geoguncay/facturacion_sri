"""
Test Script: Generate and Save Invoice XMLs
=============================================

This script demonstrates the complete flow of:
1. Create clients
2. Create products
3. Create an invoice
4. Generate the XML
5. Save the XML
6. Display the result

Usage:
    python -m app.tests.test_xml_generation
"""

import sys
import os
from datetime import datetime
from decimal import Decimal

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy.orm import Session
from app.database.db import SessionLocal, engine
from app.database import models
from app.sri.xml_generator import generate_invoice_xml, save_invoice_xml


def create_test_data(db: Session):
    """Create test clients, products and invoices."""
    
    print("\n" + "="*60)
    print("CREATING TEST DATA")
    print("="*60)
    
    # 1. Create client
    print("\n[1/5] Creating client...")
    client = models.Client(
        name="TechCorp S.A.",
        client_id="1234567890",
        address="Av. Amazonas 123, Quito",
        email="info@techcorp.ec"
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    print(f"✓ Client created: ID={client.id}, Name={client.name}")
    
    # 2. Create products
    print("\n[2/5] Creating products...")
    products_data = [
        {"name": "Premium Software License", "price": 250.00, "iva": 30.00},
        {"name": "IT Consulting", "price": 150.00, "iva": 18.00},
        {"name": "24/7 Technical Support", "price": 100.00, "iva": 12.00},
    ]
    
    products = []
    for prod_data in products_data:
        product = models.Product(
            product_name=prod_data["name"],
            price=prod_data["price"],
            iva=prod_data["iva"]
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        products.append(product)
        print(f"  ✓ {product.product_name}: ${product.price}")
    
    # 3. Create invoice details
    print("\n[3/5] Creating invoice details...")
    details_data = [
        {"producto": products[0].product_name, "cantidad": 2, "precio": 250.00, "subtotal": 500.00, "descuento": 0},
        {"producto": products[1].product_name, "cantidad": 1, "precio": 150.00, "subtotal": 150.00, "descuento": 10},
        {"producto": products[2].product_name, "cantidad": 3, "precio": 100.00, "subtotal": 300.00, "descuento": 0},
    ]
    
    subtotal = sum(d["subtotal"] for d in details_data)
    iva = round(subtotal * 0.12, 2)  # 12% VAT
    total = subtotal + iva
    
    print(f"  ✓ Subtotal: ${subtotal}")
    print(f"  ✓ VAT (12%): ${iva}")
    print(f"  ✓ Total: ${total}")
    
    # 4. Create invoice
    print("\n[4/5] Creating invoice...")
    invoice = models.Invoice(
        client_id=client.id,
        total=total,
        state="PENDING"
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    print(f"✓ Invoice created: ID={invoice.id}")
    
    # Create invoice details
    for detail_data in details_data:
        detail = models.InvoiceDetail(
            invoice_id=invoice.id,
            product=detail_data["producto"],
            quantity=detail_data["cantidad"],
            price=detail_data["precio"],
            subtotal=detail_data["subtotal"]
        )
        db.add(detail)
    db.commit()
    
    return client, products, invoice, details_data, subtotal, iva, total


def generate_invoice_xml_file(client, invoice, details_data, subtotal, iva, total):
    """Generate the invoice XML."""
    
    print("\n[5/5] Generating XML...")
    
    # Prepare data for XML
    invoice_data = {
        "razon_social": "My Company S.A.",
        "ruc": "1234567890001",
        "clave_acceso": f"{invoice.id:04d}{invoice.date.year % 100:02d}{invoice.date.month:02d}{invoice.date.day:02d}0120001000000001000000000000000000000000",
        "estab": "001",
        "pto_emision": "001",
        "secuencial": str(invoice.id),
        "fecha": invoice.date.strftime("%d/%m/%Y"),
        "direccion": client.address,
        "subtotal": subtotal,
        "iva": iva,
        "total": total,
        "detalles": details_data
    }
    
    # Generate XML
    xml_content = generate_invoice_xml(invoice_data)
    print("✓ XML generated successfully")
    
    return xml_content


def save_xml(invoice, xml_content):
    """Save the invoice XML to file."""
    
    print("\nSAVING XML...")
    print("="*60)
    
    filepath = save_invoice_xml(invoice.id, xml_content)
    
    print(f"✓ XML saved to: {filepath}")
    print(f"✓ File size: {len(xml_content)} bytes")
    
    return filepath


def display_xml(filepath):
    """Display the XML content."""
    
    print("\nXML CONTENT:")
    print("="*60)
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        print(content)


def main():
    """Main function."""
    
    print("\n" + "="*60)
    print("COMPLETE TEST: INVOICE XML GENERATION AND SAVING")
    print("="*60)
    
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # 1. Create test data
        client, products, invoice, details_data, subtotal, iva, total = create_test_data(db)
        
        # 2. Generate XML
        xml_content = generate_invoice_xml_file(client, invoice, details_data, subtotal, iva, total)
        
        # 3. Save XML
        filepath = save_xml(invoice, xml_content)
        
        # 4. Display XML
        if os.path.getsize(filepath) < 2000:  # Only show if not too large
            display_xml(filepath)
        else:
            print("(File too large to display in console)")
        
        # 5. Final summary
        print("\n" + "="*60)
        print("✅ TEST COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"\nSummary:")
        print(f"  • Client: {client.name}")
        print(f"  • Email: {client.email}")
        print(f"  • Invoice ID: {invoice.id}")
        print(f"  • Products: {len(products)}")
        print(f"  • Details: {len(details_data)}")
        print(f"  • Subtotal: ${subtotal}")
        print(f"  • VAT: ${iva}")
        print(f"  • Total: ${total}")
        print(f"  • XML saved to: {filepath}")
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"\n❌ Error during test: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()


if __name__ == "__main__":
    main()
