@echo off
echo Iniciando Sistema de Gestion de Bebidas...
echo.

REM Verificar si existen las carpetas necesarias
if not exist logs mkdir logs
if not exist graficos mkdir graficos

REM Verificar si las dependencias están instaladas
python -c "import tkinter" 2>NUL
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
)

REM Ejecutar la aplicación
python main.py

echo.
echo Presione cualquier tecla para salir...
pause > nul 