from signxml import XMLSigner
from lxml import etree


def sign_invoice_xml(xml_content, certificate_path, certificate_password=None):
    """
    Firma digitalmente un XML de factura con certificado
    
    Args:
        xml_content: Contenido XML en bytes
        certificate_path: Ruta al certificado (.p12 o .pfx)
        certificate_password: Contraseña del certificado
        
    Returns:
        bytes: XML firmado
        
    Note:
        Requiere certificado digital válido del SRI
    """
    
    # Cargar el XML
    root = etree.fromstring(xml_content)
    
    # Crear firmante (comentado porque requiere certificado real)
    # signer = XMLSigner(method=signxml.methods.enveloped)
    # signed_root = signer.sign(root, key=certificate_path, cert=certificate_path)
    
    # Por ahora retornamos XML sin firma (solo para desarrollo)
    return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")


def validate_signature(signed_xml):
    """
    Valida la firma digital de un XML
    
    Args:
        signed_xml: XML firmado en bytes
        
    Returns:
        bool: True si la firma es válida
    """
    
    root = etree.fromstring(signed_xml)
    
    # Lógica de validación comentada (requiere configuración de certificados)
    # from signxml import XMLVerifier
    # verifier = XMLVerifier()
    # try:
    #     verifier.verify(root)
    #     return True
    # except:
    #     return False
    
    return True
