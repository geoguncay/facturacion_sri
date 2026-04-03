@echo off
REM Script para resetear el proyecto a estado inicial (Windows)
REM Uso: reset.bat

echo.
echo ========================================
echo Iniciando reseteo del proyecto...
echo ========================================
echo.

REM Paso 1: Desactivar entorno virtual
echo [1/7] Desactivando entorno virtual...
call deactivate 2>nul || true

REM Paso 2: Eliminar carpeta venv
echo [2/7] Eliminando carpeta venv...
if exist venv (
    rmdir /s /q venv
    echo. Carpeta venv eliminada
) else (
    echo. venv no encontrado
)

REM Paso 3: Limpiar caché de Python
echo [3/7] Limpiando caché de Python...
for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    rmdir /s /q "%%d" 2>nul || true
)
for /d /r . %%d in (.pytest_cache) do @if exist "%%d" (
    rmdir /s /q "%%d" 2>nul || true
)
for /d /r . %%d in (.mypy_cache) do @if exist "%%d" (
    rmdir /s /q "%%d" 2>nul || true
)
echo. Caché limpiado

REM Paso 4: Eliminar archivo de base de datos
echo [4/7] Eliminando base de datos...
if exist facturacion.db (
    del /f /q facturacion.db
    echo. facturacion.db eliminado
) else (
    echo. facturacion.db no encontrado
)

REM Paso 5: Limpiar archivos .pyc
echo [5/7] Limpiando archivos .pyc...
for /r . %%f in (*.pyc) do del /f /q "%%f" 2>nul || true
for /r . %%f in (*.pyo) do del /f /q "%%f" 2>nul || true
echo. Archivos .pyc eliminados

REM Paso 6: Crear nuevo entorno virtual
echo [6/7] Creando nuevo entorno virtual...
python -m venv venv
echo. Entorno virtual creado

REM Paso 7: Activar entorno e instalar dependencias
echo [7/7] Activando entorno e instalando dependencias...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo.
echo ========================================
echo. Proyecto reseteado exitosamente!
echo ========================================
echo.
echo Proximos pasos:
echo 1. Activar entorno: venv\Scripts\activate
echo 2. Iniciar servidor: uvicorn app.main:app --reload
echo.
pause
