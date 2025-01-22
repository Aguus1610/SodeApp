import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple, Dict
import pandas as pd
from datetime import datetime, timedelta
from modelo import Venta, DetalleVenta, Cliente, Producto, Pago
from utilidades import log_operacion
from peewee import fn

class GeneradorGraficos:
    def __init__(self):
        """Inicializa el generador de gráficos con el estilo predeterminado."""
        plt.style.use('default')
        sns.set_theme()

    @log_operacion("generación_gráfico")
    def ventas_por_cliente(self, dias: int = 30) -> str:
        """
        Genera un gráfico de barras de ventas totales por cliente.
        
        Args:
            dias (int): Número de días hacia atrás para considerar
            
        Returns:
            str: Ruta del archivo guardado
        """
        fecha_inicio = datetime.now() - timedelta(days=dias)
        
        # Obtener datos
        ventas = (Venta
                 .select(Venta, Cliente)
                 .join(Cliente)
                 .where(Venta.fecha >= fecha_inicio))
        
        # Preparar datos para el gráfico
        datos = {}
        for venta in ventas:
            if venta.cliente.nombre in datos:
                datos[venta.cliente.nombre] += float(venta.total)
            else:
                datos[venta.cliente.nombre] = float(venta.total)
        
        # Crear gráfico
        plt.figure(figsize=(12, 6))
        plt.bar(datos.keys(), datos.values())
        plt.title(f'Ventas por Cliente (Últimos {dias} días)')
        plt.xticks(rotation=45)
        plt.ylabel('Total de Ventas ($)')
        
        # Guardar y retornar ruta
        ruta = f'graficos/ventas_por_cliente_{datetime.now().strftime("%Y%m%d")}.png'
        plt.savefig(ruta, bbox_inches='tight')
        plt.close()
        return ruta

    @log_operacion("generación_gráfico")
    def productos_mas_vendidos(self, top: int = 10) -> str:
        """
        Genera un gráfico de los productos más vendidos.
        
        Args:
            top (int): Cantidad de productos a mostrar
            
        Returns:
            str: Ruta del archivo guardado
        """
        # Obtener datos
        detalles = (DetalleVenta
                   .select(Producto.nombre, 
                          fn.SUM(DetalleVenta.cantidad).alias('total_vendido'))
                   .join(Producto)
                   .group_by(Producto.nombre)
                   .order_by(fn.SUM(DetalleVenta.cantidad).desc())
                   .limit(top))
        
        nombres = [d.producto.nombre for d in detalles]
        cantidades = [d.total_vendido for d in detalles]
        
        # Crear gráfico
        plt.figure(figsize=(12, 6))
        sns.barplot(x=cantidades, y=nombres)
        plt.title(f'Top {top} Productos Más Vendidos')
        plt.xlabel('Cantidad Vendida')
        
        # Guardar y retornar ruta
        ruta = f'graficos/productos_mas_vendidos_{datetime.now().strftime("%Y%m%d")}.png'
        plt.savefig(ruta, bbox_inches='tight')
        plt.close()
        return ruta

    @log_operacion("generación_gráfico")
    def tendencia_ventas(self, dias: int = 30) -> str:
        """
        Genera un gráfico de línea mostrando la tendencia de ventas.
        
        Args:
            dias (int): Número de días hacia atrás para considerar
            
        Returns:
            str: Ruta del archivo guardado
        """
        fecha_inicio = datetime.now() - timedelta(days=dias)
        
        # Obtener datos
        ventas = (Venta
                 .select(Venta.fecha, Venta.total)
                 .where(Venta.fecha >= fecha_inicio)
                 .order_by(Venta.fecha))
        
        fechas = [v.fecha for v in ventas]
        totales = [float(v.total) for v in ventas]
        
        # Crear gráfico
        plt.figure(figsize=(12, 6))
        plt.plot(fechas, totales, marker='o')
        plt.title(f'Tendencia de Ventas (Últimos {dias} días)')
        plt.xticks(rotation=45)
        plt.ylabel('Total de Ventas ($)')
        
        # Guardar y retornar ruta
        ruta = f'graficos/tendencia_ventas_{datetime.now().strftime("%Y%m%d")}.png'
        plt.savefig(ruta, bbox_inches='tight')
        plt.close()
        return ruta

    @log_operacion("generación_gráfico")
    def estado_pagos(self) -> str:
        """
        Genera un gráfico circular mostrando el estado de los pagos.
        
        Returns:
            str: Ruta del archivo guardado
        """
        # Obtener datos
        total_ventas = Venta.select(fn.COUNT(Venta.id)).scalar()
        ventas_pagadas = Venta.select(fn.COUNT(Venta.id)).where(Venta.pagada == True).scalar()
        ventas_pendientes = total_ventas - ventas_pagadas
        
        # Crear gráfico
        plt.figure(figsize=(10, 10))
        plt.pie([ventas_pagadas, ventas_pendientes],
               labels=['Pagadas', 'Pendientes'],
               autopct='%1.1f%%',
               colors=['#2ecc71', '#e74c3c'])
        plt.title('Estado de Pagos')
        
        # Guardar y retornar ruta
        ruta = f'graficos/estado_pagos_{datetime.now().strftime("%Y%m%d")}.png'
        plt.savefig(ruta, bbox_inches='tight')
        plt.close()
        return ruta 