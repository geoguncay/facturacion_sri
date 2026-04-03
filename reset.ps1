# Script para resetear el proyecto a estado inicial (PowerShell Windows)
# Uso: .\reset.ps1

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Iniciando reseteo del proyecto..." -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Paso 1: Desactivar entorno virtual
Write-Host "[1/7] Desactivando entorno virtual..." -ForegroundColor Yellow
try {
    deactivate 2>$null
} catch {
    # Continuar si no hay entorno virtual activo
}

# Paso 2: Eliminar carpeta venv
Write-Host "[2/7] Eliminando carpeta venv..." -ForegroundColor Yellow
if (Test-Path -Path "venv") {
    Remove-Item -Recurse -Force -Path "venv"
    Write-Host "✓ Carpeta venv eliminada" -ForegroundColor Green
} else {
    Write-Host "⚠ venv no encontrado" -ForegroundColor Yellow
}

# Paso 3: Limpiar caché de Python
Write-Host "[3/7] Limpiando caché de Python..." -ForegroundColor Yellow
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Directory -Filter ".pytest_cache" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Directory -Filter ".mypy_cache" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Directory -Filter "*.egg-info" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "✓ Caché limpiado" -ForegroundColor Green

# Paso 4: Eliminar archivo de base de datos
Write-Host "[4/7] Eliminando base de datos..." -ForegroundColor Yellow
if (Test-Path -Path "facturacion.db") {
    Remove-Item -Force -Path "facturacion.db"
    Write-Host "✓ facturacion.db eliminado" -ForegroundColor Green
} else {
    Write-Host "⚠ facturacion.db no encontrado" -ForegroundColor Yellow
}

# Paso 5: Limpiar archivos .pyc
Write-Host "[5/7] Limpiando archivos .pyc..." -ForegroundColor Yellow
Get-ChildItem -Recurse -File -Filter "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -File -Filter "*.pyo" | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Host "✓ Archivos .pyc eliminados" -ForegroundColor Green

# Paso 6: Crear nuevo entorno virtual
Write-Host "[6/7] Creando nuevo entorno virtual..." -ForegroundColor Yellow
python -m venv venv
Write-Host "✓ Entorno virtual creado" -ForegroundColor Green

# Paso 7: Activar entorno e instalar dependencias
Write-Host "[7/7] Activando entorno e instalando dependencias..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip setuptools wheel | Out-Null
pip install -r requirements.txt

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "✅ ¡Proyecto reseteado exitosamente!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "Próximos pasos:" -ForegroundColor Cyan
Write-Host "1. Activar entorno: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "2. Iniciar servidor: uvicorn app.main:app --reload" -ForegroundColor White
Write-Host "`n"
