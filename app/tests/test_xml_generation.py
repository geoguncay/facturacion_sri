"""
Script de Prueba: Generar y Guardar XMLs de Facturas
=====================================================

Este script demuestra el flujo completo de:
1. Crear clientes
2. Crear productos
3. Crear una factura
4. Generar el XML
5. Guardar el XML
6. Mostrar el resultado

Uso:
    python -m app.tests.test_xml_generation
"""

import sys
import os
from datetime import datetime
from decimal import Decimal

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlalchemy.orm import Session
from app.database.db import SessionLocal, engine
from app.database import models
from app.sri.xml_generator import generate_invoice_xml, save_invoice_xml


def crear_datos_prueba(db: Session):
    """Crea clientes, productos y facturas de prueba"""
    
    print("\n" + "="*60)
    print("CREANDO DATOS DE PRUEBA")
    print("="*60)
    
    # 1. Crear cliente
    print("\n[1/5] Creando cliente...")
    cliente = models.Client(
        name="TechCorp S.A.",
        identification="1234567890",
        address="Av. Amazonas 123, Quito",
        email="info@techcorp.ec"
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    print(f"✓ Cliente creado: ID={cliente.id}, Nombre={cliente.name}")
    
    # 2. Crear productos
    print("\n[2/5] Creando productos...")
    productos_data = [
        {"name": "Licencia Software Premium", "price": 250.00, "iva": 30.00},
        {"name": "Consultoría IT", "price": 150.00, "iva": 18.00},
        {"name": "Soporte Técnico 24/7", "price": 100.00, "iva": 12.00},
    ]
    
    productos = []
    for prod_data in productos_data:
        producto = models.Product(
            name_product=prod_data["name"],
            price=prod_data["price"],
            iva=prod_data["iva"]
        )
        db.add(producto)
        db.commit()
        db.refresh(producto)
        productos.append(producto)
        print(f"  ✓ {producto.name_product}: ${producto.price}")
    
    # 3. Crear detalle de facturas
    print("\n[3/5] Creando detalles de factura...")
    detalles_data = [
        {"producto": productos[0].name_product, "cantidad": 2, "precio": 250.00, "subtotal": 500.00, "descuento": 0},
        {"producto": productos[1].name_product, "cantidad": 1, "precio": 150.00, "subtotal": 150.00, "descuento": 10},
        {"producto": productos[2].name_product, "cantidad": 3, "precio": 100.00, "subtotal": 300.00, "descuento": 0},
    ]
    
    subtotal = sum(d["subtotal"] for d in detalles_data)
    iva = round(subtotal * 0.12, 2)  # IVA del 12%
    total = subtotal + iva
    
    print(f"  ✓ Subtotal: ${subtotal}")
    print(f"  ✓ IVA (12%): ${iva}")
    print(f"  ✓ Total: ${total}")
    
    # 4. Crear factura
    print("\n[4/5] Creando factura...")
    factura = models.Invoice(
        cliente_id=cliente.id,
        total=total,
        state="PENDIENTE"
    )
    db.add(factura)
    db.commit()
    db.refresh(factura)
    print(f"✓ Factura creada: ID={factura.id}")
    
    # Crear detalles de la factura
    for detalle_data in detalles_data:
        detalle = models.InvoiceDetail(
            invoice_id=factura.id,
            product=detalle_data["producto"],
            quantity=detalle_data["cantidad"],
            price=detalle_data["precio"],
            subtotal=detalle_data["subtotal"]
        )
        db.add(detalle)
    db.commit()
    
    return cliente, productos, factura, detalles_data, subtotal, iva, total


def generar_xml_factura(cliente, factura, detalles_data, subtotal, iva, total):
    """Genera el XML de la factura"""
    
    print("\n[5/5] Generando XML...")
    
    # Preparar datos para el XML
    invoice_data = {
        "razon_social": "Mi Empresa S.A.",
        "ruc": "1234567890001",
        "clave_acceso": f"{factura.id:04d}{factura.date.year % 100:02d}{factura.date.month:02d}{factura.date.day:02d}0120001000000001000000000000000000000000",
        "estab": "001",
        "pto_emision": "001",
        "secuencial": str(factura.id),
        "fecha": factura.date.strftime("%d/%m/%Y"),
        "direccion": cliente.address,
        "subtotal": subtotal,
        "iva": iva,
        "total": total,
        "detalles": detalles_data
    }
    
    # Generar XML
    xml_content = generate_invoice_xml(invoice_data)
    print("✓ XML generado exitosamente")
    
    return xml_content


def guardar_xml(factura, xml_content):
    """Guarda el XML en el sistema de archivos"""
    
    print("\nGUARDANDO XML...")
    print("="*60)
    
    filepath = save_invoice_xml(factura.id, xml_content)
    
    print(f"✓ XML guardado en: {filepath}")
    print(f"✓ Tamaño del archivo: {len(xml_content)} bytes")
    
    return filepath


def mostrar_xml(filepath):
    """Muestra el contenido del XML"""
    
    print("\nCONTENIDO DEL XML:")
    print("="*60)
    
    with open(filepath, "r", encoding="utf-8") as f:
        contenido = f.read()
        print(contenido)


def main():
    """Función principal"""
    
    print("\n" + "="*60)
    print("PRUEBA COMPLETA: GENERACIÓN Y GUARDADO DE XMLs")
    print("="*60)
    
    # Crear tablas
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # 1. Crear datos de prueba
        cliente, productos, factura, detalles_data, subtotal, iva, total = crear_datos_prueba(db)
        
        # 2. Generar XML
        xml_content = generar_xml_factura(cliente, factura, detalles_data, subtotal, iva, total)
        
        # 3. Guardar XML
        filepath = guardar_xml(factura, xml_content)
        
        # 4. Mostrar XML generado
        if os.path.getsize(filepath) < 2000:  # Solo mostrar si no es muy grande
            mostrar_xml(filepath)
        else:
            print("(Archivo muy grande para mostrar en consola)")
        
        # 5. Resumen final
        print("\n" + "="*60)
        print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
        print("="*60)
        print(f"\nResumen:")
        print(f"  • Cliente: {cliente.name}")
        print(f"  • Email: {cliente.email}")
        print(f"  • Factura ID: {factura.id}")
        print(f"  • Productos: {len(productos)}")
        print(f"  • Detalles: {len(detalles_data)}")
        print(f"  • Subtotal: ${subtotal}")
        print(f"  • IVA: ${iva}")
        print(f"  • Total: ${total}")
        print(f"  • XML guardado en: {filepath}")
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()


if __name__ == "__main__":
    main()
