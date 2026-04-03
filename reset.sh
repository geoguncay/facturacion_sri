#!/bin/bash

# Script para resetear el proyecto a estado inicial
# Uso: bash reset.sh

echo "🔄 Iniciando reseteo del proyecto..."
echo "=================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Paso 1: Desactivar entorno virtual si está activo
echo -e "${YELLOW}[1/7]${NC} Desactivando entorno virtual..."
deactivate 2>/dev/null || true

# Paso 2: Eliminar carpeta venv
echo -e "${YELLOW}[2/7]${NC} Eliminando carpeta venv..."
if [ -d "venv" ]; then
    rm -rf venv
    echo -e "${GREEN}✓ venv eliminado${NC}"
else
    echo -e "${YELLOW}⚠ venv no encontrado${NC}"
fi

# Paso 3: Limpiar caché de Python
echo -e "${YELLOW}[3/7]${NC} Limpiando caché de Python..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
echo -e "${GREEN}✓ Caché limpiado${NC}"

# Paso 4: Eliminar archivo de base de datos
echo -e "${YELLOW}[4/7]${NC} Eliminando base de datos..."
if [ -f "facturacion.db" ]; then
    rm -f facturacion.db
    echo -e "${GREEN}✓ facturacion.db eliminado${NC}"
else
    echo -e "${YELLOW}⚠ facturacion.db no encontrado${NC}"
fi

# Paso 5: Limpiar archivos .pyc
echo -e "${YELLOW}[5/7]${NC} Limpiando archivos .pyc..."
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
echo -e "${GREEN}✓ Archivos .pyc eliminados${NC}"

# Paso 6: Crear nuevo entorno virtual
echo -e "${YELLOW}[6/7]${NC} Creando nuevo entorno virtual..."
python3 -m venv venv
echo -e "${GREEN}✓ Entorno virtual creado${NC}"

# Paso 7: Activar entorno e instalar dependencias
echo -e "${YELLOW}[7/7]${NC} Activando entorno e instalando dependencias..."
source venv/bin/activate
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt

echo ""
echo "=================================="
echo -e "${GREEN}✅ ¡Proyecto reseteado exitosamente!${NC}"
echo ""
echo "Próximos pasos:"
echo "1. Activar entorno virtual: source venv/bin/activate"
echo "2. Iniciar servidor: uvicorn app.main:app --reload"
echo ""
