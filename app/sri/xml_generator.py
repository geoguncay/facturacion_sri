from lxml import etree
from datetime import datetime
import os


def generate_invoice_xml(invoice_data):
    """
    Genera un XML de factura válido para SRI Ecuador
    
    Args:
        invoice_data: Diccionario con datos de la factura
        
    Returns:
        bytes: XML codificado en UTF-8
    """
    
    # Crear elemento raíz
    invoice = etree.Element("factura")
    
    # Información Tributaria
    info_tributaria = etree.SubElement(invoice, "infoTributaria")
    etree.SubElement(info_tributaria, "razonSocial").text = invoice_data.get("razon_social", "Empresa")
    etree.SubElement(info_tributaria, "ruc").text = invoice_data.get("ruc", "1234567890001")
    etree.SubElement(info_tributaria, "claveAcceso").text = invoice_data.get("clave_acceso", "0000000000000000000000000000000000000000")
    etree.SubElement(info_tributaria, "codDoc").text = "01"  # Código de factura
    etree.SubElement(info_tributaria, "estab").text = invoice_data.get("estab", "001")
    etree.SubElement(info_tributaria, "ptoEmi").text = invoice_data.get("pto_emision", "001")
    etree.SubElement(info_tributaria, "secuencial").text = str(invoice_data.get("secuencial", "000000001")).zfill(9)
    
    # Información de la Factura
    info_factura = etree.SubElement(invoice, "infoFactura")
    etree.SubElement(info_factura, "fechaEmision").text = invoice_data.get("fecha", datetime.now().strftime("%d/%m/%Y"))
    etree.SubElement(info_factura, "dirCliente").text = invoice_data.get("direccion", "Dirección cliente")
    etree.SubElement(info_factura, "totalSinImpuestos").text = str(round(invoice_data.get("subtotal", 0), 2))
    etree.SubElement(info_factura, "totalIva").text = str(round(invoice_data.get("iva", 0), 2))
    etree.SubElement(info_factura, "importeTotal").text = str(round(invoice_data.get("total", 0), 2))
    
    # Detalles de la factura
    detalles = etree.SubElement(invoice, "detalles")
    
    for item in invoice_data.get("detalles", []):
        detalle = etree.SubElement(detalles, "detalle")
        etree.SubElement(detalle, "descripcion").text = str(item.get("producto", "Producto"))
        etree.SubElement(detalle, "cantidad").text = str(item.get("cantidad", 1))
        etree.SubElement(detalle, "precioUnitario").text = str(round(item.get("precio", 0), 2))
        etree.SubElement(detalle, "descuento").text = str(round(item.get("descuento", 0), 2))
        etree.SubElement(detalle, "precioTotalSinImpuesto").text = str(round(item.get("subtotal", 0), 2))
    
    # Convertir a bytes con formato bonito
    xml_bytes = etree.tostring(
        invoice,
        pretty_print=True,
        xml_declaration=True,
        encoding="UTF-8"
    )
    
    return xml_bytes


def save_invoice_xml(invoice_id, xml_content, output_dir="xmls"):
    """
    Guarda el XML de una factura en el sistema de archivos
    
    Args:
        invoice_id: ID de la factura
        xml_content: Contenido XML en bytes
        output_dir: Directorio donde guardar el archivo
        
    Returns:
        str: Ruta del archivo guardado
    """
    
    # Crear directorio si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Nombre del archivo
    filename = f"invoice_{invoice_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
    filepath = os.path.join(output_dir, filename)
    
    # Guardar archivo
    with open(filepath, "wb") as f:
        f.write(xml_content)
    
    return filepath
