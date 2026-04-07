from signxml import XMLSigner
from lxml import etree
import base64
from cryptography.hazmat.primitives.serialization import pkcs12

def sign_xml(xml_path, p12_path, password):

    with open(xml_path, "rb") as f:
        xml = etree.parse(f)

    with open(p12_path, "rb") as f:
        p12 = f.read()

    private_key, certificate, additional = pkcs12.load_key_and_certificates(
        p12,
        password.encode()
    )

    signer = XMLSigner()

    signed = signer.sign(
        xml,
        key=private_key,
        cert=certificate
    )

    return etree.tostring(signed)
