from lxml import etree
from datetime import datetime
import os


def generate_invoice_xml(invoice_data):
    """
    Generate a valid invoice XML for SRI Ecuador.
    
    Args:
        invoice_data: Dictionary with invoice data
        
    Returns:
        bytes: XML encoded in UTF-8
    """
    
    # Create root element
    invoice = etree.Element("factura")
    
    # Tax Information
    info_tributaria = etree.SubElement(invoice, "infoTributaria")
    etree.SubElement(info_tributaria, "razonSocial").text = invoice_data.get("razon_social", "Empresa")
    etree.SubElement(info_tributaria, "ruc").text = invoice_data.get("ruc", "1234567890001")
    etree.SubElement(info_tributaria, "claveAcceso").text = invoice_data.get("clave_acceso", "0000000000000000000000000000000000000000")
    etree.SubElement(info_tributaria, "codDoc").text = "01"  # Invoice code
    etree.SubElement(info_tributaria, "estab").text = invoice_data.get("estab", "001")
    etree.SubElement(info_tributaria, "ptoEmi").text = invoice_data.get("pto_emision", "001")
    etree.SubElement(info_tributaria, "secuencial").text = str(invoice_data.get("secuencial", "000000001")).zfill(9)
    
    # Invoice Information
    info_factura = etree.SubElement(invoice, "infoFactura")
    etree.SubElement(info_factura, "fechaEmision").text = invoice_data.get("fecha", datetime.now().strftime("%d/%m/%Y"))
    etree.SubElement(info_factura, "dirCliente").text = invoice_data.get("direccion", "Customer address")
    etree.SubElement(info_factura, "totalSinImpuestos").text = str(round(invoice_data.get("subtotal", 0), 2))
    etree.SubElement(info_factura, "totalIva").text = str(round(invoice_data.get("iva", 0), 2))
    etree.SubElement(info_factura, "importeTotal").text = str(round(invoice_data.get("total", 0), 2))
    
    # Invoice Details
    detalles = etree.SubElement(invoice, "detalles")
    
    for item in invoice_data.get("detalles", []):
        detalle = etree.SubElement(detalles, "detalle")
        etree.SubElement(detalle, "descripcion").text = str(item.get("producto", "Product"))
        etree.SubElement(detalle, "cantidad").text = str(item.get("cantidad", 1))
        etree.SubElement(detalle, "precioUnitario").text = str(round(item.get("precio", 0), 2))
        etree.SubElement(detalle, "descuento").text = str(round(item.get("descuento", 0), 2))
        etree.SubElement(detalle, "precioTotalSinImpuesto").text = str(round(item.get("subtotal", 0), 2))
    
    # Convert to bytes with nice formatting
    xml_bytes = etree.tostring(
        invoice,
        pretty_print=True,
        xml_declaration=True,
        encoding="UTF-8"
    )
    
    return xml_bytes


def save_invoice_xml(invoice_id, xml_content, output_dir="xmls"):
    """
    Save an invoice XML to the file system.
    
    Args:
        invoice_id: Invoice ID
        xml_content: XML content in bytes
        output_dir: Directory where to save the file
        
    Returns:
        str: Path to the saved file
    """
    
    # Create directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Filename
    filename = f"invoice_{invoice_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
    filepath = os.path.join(output_dir, filename)
    
    # Save file
    with open(filepath, "wb") as f:
        f.write(xml_content)
    
    return filepath
