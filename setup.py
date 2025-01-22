import sys
from cx_Freeze import setup, Executable

# Dependencias
build_exe_options = {
    "packages": ["tkinter", "peewee", "matplotlib", "seaborn", "pandas"],
    "includes": ["PIL", "decimal", "datetime"],
    "include_files": [
        "manual_usuario.md",
        "logs/",
        "graficos/"
    ],
    "excludes": ["test", "unittest"],
}

# Configuración del ejecutable
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Sistema de Gestión de Bebidas",
    version="1.0",
    description="Sistema para gestión de distribuidora de bebidas",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py",
            base=base,
            target_name="GestionBebidas.exe",
            icon="icono.ico",  # Asegúrate de tener un archivo de icono
            shortcut_name="Sistema de Gestión de Bebidas",
            shortcut_dir="DesktopFolder"
        )
    ]
) 