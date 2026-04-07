from zeep import Client
import base64


class SRIClient:
    def __init__(self):
        self.reception_wsdl = "https://celcer.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline?wsdl"
        self.authorization_wsdl = "https://celcer.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline?wsdl"
        self.reception_client = Client(self.reception_wsdl)
        self.authorization_client = Client(self.authorization_wsdl)

    def send_invoice(self, xml):
        xml_base64 = base64.b64encode(xml).decode()
        response = self.reception_client.service.validarComprobante(xml_base64)
        return response

    def consult_authorization(self, access_key):
        response = self.authorization_client.service.autorizacionComprobante(
            access_key=access_key
        )

        return response