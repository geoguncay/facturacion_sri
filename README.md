# Sistema de Facturación SRI

Sistema de facturación electrónica integrado con el Servicio de Rentas Internas (SRI) de Ecuador. Esta aplicación permite gestionar clientes, productos, facturas y la generación de documentos XML firmados para el SRI.

## 📋 Descripción del Proyecto

API desarrollada con **FastAPI** para la gestión completa de facturación electrónica, incluyendo:

- ✅ Gestión de clientes
- ✅ Gestión de productos
- ✅ Generación de facturas
- ✅ Generación de XML firmados digitalmente
- ✅ Generación de reportes en PDF
- ✅ Integración con servicios del SRI

## 🛠️ Tecnologías Utilizadas

- **FastAPI** - Framework web moderno para APIs
- **SQLAlchemy** - ORM para bases de datos
- **Pydantic** - Validación de datos
- **SQLite** - Base de datos
- **lxml** - Procesamiento de XML
- **zeep** - Cliente SOAP para web services
- **signxml** - Firma digital de documentos XML
- **reportlab** - Generación de PDFs
- **Uvicorn** - Servidor ASGI

## 📦 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Virtual environment (venv)

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd facturacion_sri
```

### 2. Crear y Activar el Entorno Virtual

#### En macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### En Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

1. Asegúrate de que la carpeta `app/` existe con la estructura correcta
2. Las dependencias de SQLAlchemy crearán automáticamente la base de datos SQLite en `facturacion.db`
3. Configura tus variables de entorno si es necesario (certificados digitales, credenciales SRI, etc.)

## 🔄 Resetear Proyecto a Estado Inicial

Si deseas eliminar el entorno virtual, la base de datos y todas las carpetas temporales para iniciar el proyecto desde cero, utiliza uno de estos scripts:

### En macOS/Linux:

```bash
bash reset.sh
```

### En Windows (Command Prompt):

```bash
reset.bat
```

### En Windows (PowerShell):

```powershell
.\reset.ps1
```

**Qué hace el script de reseteo:**
- ✅ Desactiva el entorno virtual (si está activo)
- ✅ Elimina la carpeta `venv/` completa
- ✅ Limpia caché de Python (`__pycache__`, `.pytest_cache`, `.mypy_cache`)
- ✅ Elimina la base de datos (`facturacion.db`)
- ✅ Elimina archivos compilados (`.pyc`, `.pyo`)
- ✅ Crea un nuevo entorno virtual
- ✅ Instala todas las dependencias nuevamente

**Resultado:** Tu proyecto quedará como si fuera la primera vez que lo instalas.

## 📁 Estructura del Proyecto

```
facturacion_sri/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada de la aplicación
│   ├── config.py               # Configuraciones
│   ├── api/                    # Rutas de la API
│   │   ├── client.py           # Endpoint de clientes
│   │   ├── invoice.py          # Endpoint de facturas
│   │   └── product.py          # Endpoint de productos
│   ├── database/               # Capas de datos
│   │   ├── db.py               # Configuración de base de datos
│   │   └── models.py           # Modelos de SQLAlchemy
│   ├── pdf/                    # Generación de reportes
│   │   └── ride_generator.py   # Generador de RIDE (Representación Impresa)
│   ├── schemas/                # Esquemas Pydantic
│   │   ├── client_schema.py
│   │   ├── invoice_schema.py
│   │   └── product_schema.py
│   ├── services/               # Lógica de negocio
│   │   ├── service_invoice.py
│   │   └── sri_service.py
│   └── sri/                    # Integración SRI
│       ├── sri_client.py       # Cliente SRI
│       ├── xml_generator.py    # Generador de XML
│       └── xml_signer.py       # Firma de XML
├── requirements.txt            # Dependencias del proyecto
├── .gitignore                  # Archivos a ignorar en Git
└── README.md                   # Este archivo
```

## 🔧 Uso

### Iniciar el Servidor de Desarrollo

```bash
uvicorn app.main:app --reload
```

El servidor se iniciará en: `http://127.0.0.1:8000`

### Acceder a la Documentación Interactiva

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Endpoints Principales

#### Clientes
- `GET /clients/` - Listar todos los clientes
- `POST /clients/` - Crear un nuevo cliente

#### Productos
- `GET /products/` - Listar todos los productos
- `POST /products/` - Crear un nuevo producto

#### Facturas
- `GET /invoices/` - Listar todas las facturas
- `POST /invoices/` - Crear una nueva factura

## 📝 Ejemplo de Uso con cURL

### Crear un Cliente
```bash
curl -X POST "http://127.0.0.1:8000/clients/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Empresa XYZ",
    "identification": "1234567890",
    "address": "Calle Principal 123",
    "email": "info@empresa.ec"
  }'
```

### Listar Clientes
```bash
curl -X GET "http://127.0.0.1:8000/clients/"
```

## 🗑️ Desinstalación de Dependencias

### Opción 1: Desinstalar Todo a la Vez

Para desinstalar **todas** las dependencias instaladas en el entorno virtual:

```bash
pip uninstall -r requirements.txt -y
```

### Opción 2: Desinstalar Paquete Individual

Si deseas desinstalar un paquete específico:

```bash
# Ejemplo: desinstalar FastAPI
pip uninstall fastapi -y
```

### Opción 3: Limpiar el Entorno Virtual Completamente

Para limpiar completamente el entorno virtual y empezar desde cero:

```bash
# 1. Desactivar el entorno virtual (si está activo)
deactivate

# 2. Eliminar la carpeta del entorno virtual
rm -rf venv  # En macOS/Linux
rmdir /s venv  # En Windows (cmd)
Remove-Item -Recurse -Force venv  # En Windows (PowerShell)

# 3. Crear un nuevo entorno virtual
python3 -m venv venv

# 4. Activar el nuevo entorno
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 5. Instalar las dependencias nuevamente
pip install -r requirements.txt
```

### Opción 4: Listar Dependencias Instaladas

Para ver todas las dependencias actualmente instaladas:

```bash
pip list
```

### Opción 5: Generar Archivo de Dependencias Actualizado

Si modificaste el entorno y deseas actualizar el archivo `requirements.txt`:

```bash
pip freeze > requirements.txt
```

## 🔒 Variables de Entorno (Opcional)

Crear un archivo `.env` en la raíz del proyecto (ejemplo):

```env
DATABASE_URL=sqlite:///./facturacion.db
API_TITLE=Sistema de Facturación SRI
DEBUG=True
```

## 🤝 Contribución

1. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
2. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
3. Push a la rama (`git push origin feature/AmazingFeature`)
4. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👤 Autor

Desarrollado para la gestión de facturación electrónica SRI Ecuador.

## 📞 Soporte

Para reportar problemas o sugerencias, por favor abre un issue en el repositorio.

## 🔄 Cambios Recientes

### v1.0.0
- Corrección de relaciones SQLAlchemy en el modelo Client
- Implementación de estructura base de la API
- Documentación inicial del proyecto

---

**Última actualización**: Abril 2026
