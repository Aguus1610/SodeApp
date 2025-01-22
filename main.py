import tkinter as tk
import os
from vista import VistaPrincipal
from controlador import Controlador
from modelo import inicializar_db
from utilidades import configurar_logging
from graficos import GeneradorGraficos

def main():
    """Función principal que inicia la aplicación."""
    
    # Crear directorios necesarios
    for directorio in ['logs', 'graficos']:
        if not os.path.exists(directorio):
            os.makedirs(directorio)
    
    # Inicializar base de datos
    inicializar_db()
    
    # Configurar logging
    configurar_logging()
    
    # Crear ventana principal
    root = tk.Tk()
    app = VistaPrincipal(root)
    
    # Inicializar controlador y generador de gráficos
    controlador = Controlador()
    graficos = GeneradorGraficos()
    
    # Configurar tema y estilo
    root.option_add('*tearOff', False)  # Deshabilitar menús desprendibles
    
    # Iniciar loop principal
    root.mainloop()

if __name__ == '__main__':
    main() 