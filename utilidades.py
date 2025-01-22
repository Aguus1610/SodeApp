import logging
from datetime import datetime
from functools import wraps
from typing import Callable, Any
import os

# Configuración del sistema de logging
def configurar_logging():
    """Configura el sistema de logging para la aplicación."""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    logging.basicConfig(
        filename=f'logs/app_{datetime.now().strftime("%Y%m%d")}.log',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

# Decorador para logging de operaciones
def log_operacion(operacion: str):
    """
    Decorador para registrar operaciones en el log.
    
    Args:
        operacion (str): Nombre de la operación a registrar
    """
    def decorador(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                resultado = func(*args, **kwargs)
                logging.info(f'Operación exitosa: {operacion} - Función: {func.__name__}')
                return resultado
            except Exception as e:
                logging.error(f'Error en operación {operacion} - Función: {func.__name__} - Error: {str(e)}')
                raise
        return wrapper
    return decorador

def validar_telefono(telefono: str) -> bool:
    """
    Valida que el número de teléfono tenga un formato válido.
    Acepta formatos como:
    - 1123456789
    - 11-2345-6789
    - (11) 2345-6789
    - +54 11 2345-6789
    
    Args:
        telefono (str): Número de teléfono a validar
        
    Returns:
        bool: True si el formato es válido, False en caso contrario
    """
    import re
    # Eliminar espacios, paréntesis y guiones para contar dígitos
    solo_numeros = re.sub(r'[\s\(\)\-\+]', '', telefono)
    
    # Verificar que tenga entre 8 y 15 dígitos (para incluir código de país)
    if not (8 <= len(solo_numeros) <= 15):
        return False
    
    # Verificar que solo contenga caracteres válidos
    patron = r'^[\+]?[\d\s\(\)\-]+$'
    return bool(re.match(patron, telefono))

def validar_email(email: str) -> bool:
    """
    Valida que el email tenga un formato válido.
    
    Args:
        email (str): Email a validar
        
    Returns:
        bool: True si el formato es válido, False en caso contrario
    """
    import re
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron, email))

def formatear_moneda(valor: float) -> str:
    """
    Formatea un valor numérico como moneda.
    
    Args:
        valor (float): Valor a formatear
        
    Returns:
        str: Valor formateado como moneda
    """
    return f"${valor:,.2f}"

def calcular_total_venta(cantidad: int, precio_unitario: float) -> float:
    """
    Calcula el total de una venta.
    
    Args:
        cantidad (int): Cantidad de productos
        precio_unitario (float): Precio unitario del producto
        
    Returns:
        float: Total calculado
    """
    return round(cantidad * precio_unitario, 2)

# Inicializar logging al importar el módulo
configurar_logging() 