@echo off
echo Instalando Sistema de Gestion de Bebidas...
echo.

REM Crear directorios necesarios
if not exist "logs" mkdir logs
if not exist "graficos" mkdir graficos

REM Instalar dependencias
pip install -r requirements.txt

REM Instalar cx_Freeze para el empaquetado
pip install cx_Freeze

REM Generar el ejecutable
python setup.py build

echo.
echo Instalacion completada!
echo El ejecutable se encuentra en la carpeta "build"
echo.
pause 