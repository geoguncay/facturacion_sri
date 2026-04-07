# Guide: Invoice XML Generation and Storage

## 📋 Description

This document explains how to generate, sign, and save valid electronic invoice XMLs for SRI Ecuador.

## 🏗️ System Architecture

The XML generation system is divided into three modules:

```
app/sri/
├── xml_generator.py    # Generates XMLs
├── xml_signer.py       # Digitally signs XMLs
└── sri_client.py       # Client for SRI services
```

## 📊 Process Flow

```
1. Create Client
   ↓
2. Create Products
   ↓
3. Create Invoice
   ↓
4. Generate XML
   ↓
5. Sign XML (optional)
   ↓
6. Save XML
   ↓
7. Send to SRI (production)
```

## 🧪 Run Complete Test

To test the entire process automatically, run:

### macOS/Linux:
```bash
cd facturacion_sri
source venv/bin/activate
python -m app.tests.test_xml_generation
```

### Windows:
```bash
cd facturacion_sri
venv\Scripts\activate
python -m app.tests.test_xml_generation
```

### Qué hace la prueba:

1. ✅ Crea 1 cliente de prueba
2. ✅ Crea 3 productos
3. ✅ Crea 1 factura con 3 detalles
4. ✅ Calcula subtotal, IVA y total
5. ✅ Genera el XML de la factura
6. ✅ Guarda el XML en `xmls/invoice_1_20260402_231114.xml`
7. ✅ Muestra el XML en la consola

### Resultado esperado:

```
============================================================
✅ PRUEBA COMPLETADA EXITOSAMENTE
============================================================

Resumen:
  • Cliente: TechCorp S.A.
  • Email: info@techcorp.ec
  • Factura ID: 1
  • Productos: 3
  • Detalles: 3
  • Subtotal: $950.0
  • IVA: $114.0
  • Total: $1064.0
  • XML guardado en: xmls/invoice_1_20260402_231114.xml
```

## 💻 Usar en la API

### 1. Crear una Factura

```bash
curl -X POST "http://127.0.0.1:8000/invoices/" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": 1,
    "details": [
      {
        "product": "Servicio A",
        "quantity": 2,
        "price": 100.00
      },
      {
        "product": "Servicio B",
        "quantity": 1,
        "price": 50.00
      }
    ]
  }'
```

### 2. Generar XML Programáticamente

```python
from app.sri.xml_generator import generate_invoice_xml, save_invoice_xml

# Datos de la factura
invoice_data = {
    "razon_social": "Mi Empresa",
    "ruc": "1234567890001",
    "clave_acceso": "1234567890012300100001000000000010000000001",
    "estab": "001",
    "pto_emision": "001",
    "secuencial": "000000001",
    "fecha": "03/04/2026",
    "direccion": "Quito, Ecuador",
    "subtotal": 200.00,
    "iva": 24.00,
    "total": 224.00,
    "detalles": [
        {
            "producto": "Servicio A",
            "cantidad": 2,
            "precio": 100.00,
            "subtotal": 200.00,
            "descuento": 0
        }
    ]
}

# Generar XML
xml_content = generate_invoice_xml(invoice_data)

# Guardar XML
filepath = save_invoice_xml(invoice_id=1, xml_content=xml_content)
print(f"XML guardado en: {filepath}")
```

## 📁 Estructura del XML Generado

```xml
<?xml version='1.0' encoding='UTF-8'?>
<factura>
  <infoTributaria>
    <razonSocial>Mi Empresa S.A.</razonSocial>
    <ruc>1234567890001</ruc>
    <claveAcceso>0001260403...</claveAcceso>
    <codDoc>01</codDoc>  <!-- Código de factura -->
    <estab>001</estab>
    <ptoEmi>001</ptoEmi>
    <secuencial>000000001</secuencial>
  </infoTributaria>
  <infoFactura>
    <fechaEmision>03/04/2026</fechaEmision>
    <dirCliente>Quito, Ecuador</dirCliente>
    <totalSinImpuestos>950.0</totalSinImpuestos>
    <totalIva>114.0</totalIva>
    <importeTotal>1064.0</importeTotal>
  </infoFactura>
  <detalles>
    <detalle>
      <descripcion>Producto A</descripcion>
      <cantidad>2</cantidad>
      <precioUnitario>100.00</precioUnitario>
      <descuento>0</descuento>
      <precioTotalSinImpuesto>200.00</precioTotalSinImpuesto>
    </detalle>
  </detalles>
</factura>
```

## 🔐 Firmar XML (Próxima Fase)

Actualmente el sistema está implementado para generar XMLs sin firma. Para agregar firma digital:

### 1. Obtener Certificado Digital

- Solicitar certificado al SRI
- Formato: `.p12` o `.pfx`
- Guardar en carpeta segura: `certs/`

### 2. Implementar Firma

```python
from app.sri.xml_signer import sign_invoice_xml

# Firmar XML
signed_xml = sign_invoice_xml(
    xml_content=xml_content,
    certificate_path="certs/certificado.p12",
    certificate_password="mi_contraseña"
)

# Guardar XML firmado
filepath = save_invoice_xml(invoice_id=1, xml_content=signed_xml)
```

## 📊 Códigos de Documento SRI

| Código | Documento |
|--------|-----------|
| 01 | Factura |
| 02 | Nota de Crédito |
| 03 | Nota de Débito |
| 04 | Nota de Venta |

## 🔑 Campos Obligatorios del XML

| Campo | Obligatorio | Descripción |
|-------|-------------|-----------|
| razonSocial | ✓ | Nombre legal de la empresa |
| ruc | ✓ | RUC de la empresa (13 dígitos) |
| claveAcceso | ✓ | 43 dígitos para identificación |
| codDoc | ✓ | Código del tipo de documento |
| estab | ✓ | Establecimiento (00-99) |
| ptoEmi | ✓ | Punto de emisión (00-99) |
| secuencial | ✓ | Número secuencial (001-999999999) |
| fechaEmision | ✓ | Fecha DD/MM/YYYY |
| detalles | ✓ | Al menos 1 detalle |

## 🔍 Validar XML

### Desde Python:

```python
from lxml import etree

# Cargar XML
tree = etree.parse('xmls/invoice_1.xml')
root = tree.getroot()

# Validar estructura
if root.tag == 'factura':
    print("✓ Estructura XML válida")
else:
    print("✗ Estructura XML inválida")
```

### Desde Terminal:

```bash
# Ver contenido del XML
cat xmls/invoice_1_20260402_231114.xml

# Contar elementos
grep -o "<detalle>" xmls/invoice_1_20260402_231114.xml | wc -l
```

## 📍 Ubicación de XMLs Generados

Los XMLs se guardan automáticamente en:

```
facturacion_sri/
└── xmls/
    ├── invoice_1_20260402_231114.xml
    ├── invoice_2_20260402_232305.xml
    └── invoice_3_20260402_233456.xml
```

**Nombre de archivo**: `invoice_{id}_{fecha_hora}.xml`

## 🚀 Próximas Mejoras

- [ ] Implementar firma digital con certificado SRI
- [ ] Validación de claveAcceso en tiempo real
- [ ] Integración con servicios de consulta SRI
- [ ] Generación de PDF RIDE (Representación Impresa)
- [ ] Almacenamiento de XMLs en base de datos

## 🆘 Solución de Problemas

### Problema 1: "ModuleNotFoundError: No module named 'lxml'"

```bash
pip install lxml
```

### Problema 2: "Database is locked"

Este error ocurre cuando hay múltiples accesos simultáneos a SQLite:

```bash
# Reiniciar con nueva base de datos
bash reset.sh
```

### Problema 3: "XML malformed"

Verifica que:
- ✓ Todos los campos requeridos existan
- ✓ Las fechas estén en formato DD/MM/YYYY
- ✓ Los números sean formato float válido
- ✓ No haya caracteres especiales sin escapar

```python
# Validar datos antes de generar
from lxml import etree

try:
    xml_content = generate_invoice_xml(invoice_data)
    tree = etree.fromstring(xml_content)
    print("✓ XML válido")
except etree.XMLSyntaxError as e:
    print(f"✗ Error en XML: {e}")
```

## 📞 Recursos Útiles

- [Documentación SRI Ecuador](https://www.sri.gob.ec)
- [Especificaciones de Factura Electrónica](https://www.sri.gob.ec/factura-electronica)
- [lxml Documentation](https://lxml.de/)
- [Python datetime](https://docs.python.org/3/library/datetime.html)

---

**Última actualización**: Abril 2026
**Versión**: 1.0.0
