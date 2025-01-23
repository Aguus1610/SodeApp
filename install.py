import subprocess
import sys
import os
import platform

def ejecutar_comando(comando, shell=False):
    try:
        subprocess.run(comando, shell=shell, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando comando: {e}")
        print(f"Salida de error: {e.stderr}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def crear_ejecutable():
    print("Creando ejecutable...")
    
    try:
        # Limpiar directorios anteriores
        import shutil
        if os.path.exists('build'):
            shutil.rmtree('build')
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        if os.path.exists('GestionBebidas.spec'):
            os.remove('GestionBebidas.spec')

        # Comando directo de PyInstaller
        comando = [
            sys.executable,
            '-m',
            'PyInstaller',
            '--name=GestionBebidas',
            '--windowed',
            '--onedir',
            '--clean',
            # Archivos principales
            '--add-data=vista.py;.',
            '--add-data=modelo.py;.',
            '--add-data=controlador.py;.',
            '--add-data=graficos.py;.',
            '--add-data=utilidades.py;.',
            # Imports de Kivy
            '--hidden-import=kivy',
            '--hidden-import=kivy.core.window.window_sdl2',
            '--hidden-import=kivy.core.text.text_sdl2',
            '--hidden-import=kivy.core.text.markup',
            '--hidden-import=kivy.core.image',
            '--hidden-import=kivy.core.audio.audio_sdl2',
            '--hidden-import=kivy.uix.behaviors',
            '--hidden-import=kivy.uix.recycleview',
            '--hidden-import=kivy.factory_registers',
            '--hidden-import=kivy.graphics',
            '--hidden-import=kivy.graphics.texture',
            '--hidden-import=kivy.graphics.vertex',
            '--hidden-import=kivy.graphics.compiler',
            '--hidden-import=kivy.loader',
            '--hidden-import=kivy.support',
            '--hidden-import=kivy.core.clipboard',
            '--hidden-import=kivy.core.clipboard.clipboard_sdl2',
            # Imports de KivyMD
            '--hidden-import=kivymd',
            '--hidden-import=kivymd.uix.behaviors',
            '--hidden-import=kivymd.uix.dialog',
            '--hidden-import=kivymd.uix.button',
            '--hidden-import=kivymd.uix.list',
            '--hidden-import=kivymd.icon_definitions',
            # Otros imports necesarios
            '--hidden-import=PIL',
            '--hidden-import=PIL._imagingtk',
            '--hidden-import=PIL._tkinter_finder',
            '--hidden-import=peewee',
            '--hidden-import=pandas',
            '--hidden-import=numpy',
            '--hidden-import=tkinter',
            # Excluir módulos innecesarios
            '--exclude-module=tensorflow',
            '--exclude-module=torch',
            '--exclude-module=scipy',
            '--exclude-module=sphinx',
            '--exclude-module=keras',
            '--exclude-module=pyarrow',
            '--exclude-module=pygments',
            '--exclude-module=IPython',
            '--exclude-module=jupyter',
            '--exclude-module=docutils',
            '--exclude-module=colorama',
            # Archivo principal
            'main.py'
        ]

        # Remover --exclude-module=_tkinter del comando
        comando = [x for x in comando if not x.endswith('_tkinter')]

        print("Ejecutando PyInstaller...")
        resultado = ejecutar_comando(comando)
        
        if resultado:
            print("\nEjecutable creado exitosamente!")
            print("Puedes encontrarlo en la carpeta 'dist/GestionBebidas'")
            return True
        else:
            print("\nError al crear el ejecutable")
            return False
            
    except Exception as e:
        print(f"Error al crear el ejecutable: {e}")
        return False

def main():
    print("=== Instalador de Gestión de Bebidas ===")
    
    while True:
        print("\n1. Instalar dependencias")
        print("2. Crear ejecutable")
        print("3. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            print("Instalando dependencias...")
            ejecutar_comando([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        elif opcion == "2":
            crear_ejecutable()
        elif opcion == "3":
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main() 