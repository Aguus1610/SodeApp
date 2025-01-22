from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime
from decimal import Decimal
from peewee import fn, JOIN, SQL

from modelo import (
    db, Cliente, Producto, Proveedor, 
    Venta, DetalleVenta, Pago
)
from utilidades import log_operacion, validar_email, validar_telefono

class Controlador:
    # CRUD Clientes
    @log_operacion("gestión_cliente")
    def agregar_cliente(self, nombre: str, telefono: str, direccion: str, 
                       email: Optional[str] = None, limite_credito: float = 0) -> Cliente:
        """
        Agrega un nuevo cliente a la base de datos.
        
        Args:
            nombre (str): Nombre del cliente
            telefono (str): Teléfono del cliente
            direccion (str): Dirección del cliente
            email (Optional[str]): Email del cliente
            limite_credito (float): Límite de crédito del cliente
            
        Returns:
            Cliente: Instancia del cliente creado
        """
        if email and not validar_email(email):
            raise ValueError("Email inválido")
        if not validar_telefono(telefono):
            raise ValueError("Teléfono inválido")
            
        with db.atomic():
            cliente = Cliente.create(
                nombre=nombre,
                telefono=telefono,
                direccion=direccion,
                email=email,
                limite_credito=limite_credito
            )
        return cliente

    @log_operacion("gestión_cliente")
    def actualizar_cliente(self, cliente_id: int, **datos) -> Cliente:
        """Actualiza los datos de un cliente existente."""
        if 'email' in datos and datos['email'] and not validar_email(datos['email']):
            raise ValueError("Email inválido")
        if 'telefono' in datos and not validar_telefono(datos['telefono']):
            raise ValueError("Teléfono inválido")
        
        with db.atomic():
            cliente = Cliente.get_by_id(cliente_id)
            for campo, valor in datos.items():
                setattr(cliente, campo, valor)
            cliente.save()
        return cliente

    @log_operacion("gestión_cliente")
    def eliminar_cliente(self, cliente_id: int) -> bool:
        """Elimina (desactiva) un cliente."""
        with db.atomic():
            cliente = Cliente.get_by_id(cliente_id)
            cliente.activo = False
            cliente.save()
            return True

    # CRUD Productos
    @log_operacion("gestión_producto")
    def agregar_producto(self, nombre: str, precio: float, stock: int,
                        proveedor_id: int, descripcion: Optional[str] = None,
                        stock_minimo: int = 10) -> Producto:
        """
        Agrega un nuevo producto al inventario.
        
        Args:
            nombre (str): Nombre del producto
            precio (float): Precio unitario
            stock (int): Cantidad inicial en stock
            proveedor_id (int): ID del proveedor
            descripcion (Optional[str]): Descripción del producto
            stock_minimo (int): Cantidad mínima antes de alertar
            
        Returns:
            Producto: Instancia del producto creado
        """
        with db.atomic():
            producto = Producto.create(
                nombre=nombre,
                precio_unitario=precio,
                stock_actual=stock,
                stock_minimo=stock_minimo,
                proveedor_id=proveedor_id,
                descripcion=descripcion
            )
        return producto

    @log_operacion("gestión_producto")
    def actualizar_producto(self, producto_id: int, **datos) -> Producto:
        """Actualiza los datos de un producto existente."""
        with db.atomic():
            producto = Producto.get_by_id(producto_id)
            for campo, valor in datos.items():
                setattr(producto, campo, valor)
            producto.save()
        return producto

    @log_operacion("gestión_producto")
    def eliminar_producto(self, producto_id: int) -> bool:
        """Elimina (desactiva) un producto."""
        with db.atomic():
            producto = Producto.get_by_id(producto_id)
            producto.activo = False
            producto.save()
            return True

    @log_operacion("gestión_producto")
    def ajustar_stock(self, producto_id: int, cantidad: int, motivo: str) -> Producto:
        """Ajusta el stock de un producto."""
        with db.atomic():
            producto = Producto.get_by_id(producto_id)
            producto.stock_actual += cantidad
            if producto.stock_actual < 0:
                raise ValueError("El stock no puede ser negativo")
            producto.save()
            return producto

    # CRUD Proveedores
    @log_operacion("gestión_proveedor")
    def agregar_proveedor(self, nombre: str, telefono: str, 
                         email: Optional[str] = None, direccion: Optional[str] = None) -> Proveedor:
        """Agrega un nuevo proveedor."""
        if email and not validar_email(email):
            raise ValueError("Email inválido")
        if not validar_telefono(telefono):
            raise ValueError("Teléfono inválido")
            
        with db.atomic():
            proveedor = Proveedor.create(
                nombre=nombre,
                telefono=telefono,
                email=email,
                direccion=direccion
            )
        return proveedor

    @log_operacion("gestión_proveedor")
    def actualizar_proveedor(self, proveedor_id: int, **datos) -> Proveedor:
        """Actualiza los datos de un proveedor existente."""
        if 'email' in datos and datos['email'] and not validar_email(datos['email']):
            raise ValueError("Email inválido")
        if 'telefono' in datos and not validar_telefono(datos['telefono']):
            raise ValueError("Teléfono inválido")
        
        with db.atomic():
            proveedor = Proveedor.get_by_id(proveedor_id)
            for campo, valor in datos.items():
                setattr(proveedor, campo, valor)
            proveedor.save()
        return proveedor

    @log_operacion("gestión_proveedor")
    def eliminar_proveedor(self, proveedor_id: int) -> bool:
        """Elimina (desactiva) un proveedor."""
        with db.atomic():
            proveedor = Proveedor.get_by_id(proveedor_id)
            proveedor.activo = False
            proveedor.save()
            return True

    # Métodos de consulta
    @log_operacion("consulta")
    def obtener_todos_clientes(self) -> List[Cliente]:
        """
        Obtiene todos los clientes activos ordenados por nombre.
        
        Returns:
            List[Cliente]: Lista de clientes activos
        """
        return (Cliente
                .select()
                .where(Cliente.activo == True)
                .order_by(Cliente.nombre))

    @log_operacion("consulta")
    def obtener_todos_productos(self) -> List[Producto]:
        return (Producto
                .select()
                .where(Producto.activo == True)
                .order_by(Producto.nombre))

    @log_operacion("consulta")
    def obtener_todos_proveedores(self) -> List[Proveedor]:
        return (Proveedor
                .select()
                .where(Proveedor.activo == True)
                .order_by(Proveedor.nombre))

    @log_operacion("consulta")
    def buscar_clientes(self, texto: str) -> List[Cliente]:
        """
        Busca clientes por nombre, teléfono o email.
        
        Args:
            texto (str): Texto a buscar
            
        Returns:
            List[Cliente]: Lista de clientes que coinciden con la búsqueda
        """
        texto = f"%{texto}%"
        return (Cliente
                .select()
                .where(
                    (Cliente.activo == True) &
                    (
                        (Cliente.nombre ** texto) |
                        (Cliente.telefono ** texto) |
                        (Cliente.email ** texto)
                    )
                )
                .order_by(Cliente.nombre))

    @log_operacion("consulta")
    def buscar_productos(self, texto: str) -> List[Producto]:
        """Busca productos por nombre o descripción."""
        texto = f"%{texto}%"
        return (Producto
                .select()
                .where(
                    (Producto.activo == True) &
                    (
                        (Producto.nombre ** texto) |
                        (Producto.descripcion ** texto)
                    )
                )
                .order_by(Producto.nombre))

    @log_operacion("consulta")
    def buscar_proveedores(self, texto: str) -> List[Proveedor]:
        """Busca proveedores por nombre, teléfono o email."""
        texto = f"%{texto}%"
        return (Proveedor
                .select()
                .where(
                    (Proveedor.activo == True) &
                    (
                        (Proveedor.nombre ** texto) |
                        (Proveedor.telefono ** texto) |
                        (Proveedor.email ** texto)
                    )
                )
                .order_by(Proveedor.nombre))

    # Gestión de Ventas
    @log_operacion("gestión_venta")
    def registrar_venta(self, cliente_id: int, 
                       items: List[Dict[str, int]]) -> Tuple[Venta, List[DetalleVenta]]:
        """
        Registra una nueva venta.
        
        Args:
            cliente_id (int): ID del cliente
            items (List[Dict[str, int]]): Lista de productos y cantidades
                [{"producto_id": id, "cantidad": cantidad}, ...]
            
        Returns:
            Tuple[Venta, List[DetalleVenta]]: Venta y sus detalles
        """
        with db.atomic():
            # Crear venta
            venta = Venta.create(
                cliente_id=cliente_id,
                fecha=datetime.now(),
                total=0
            )
            
            detalles = []
            total_venta = Decimal('0')
            
            # Procesar cada item
            for item in items:
                producto = Producto.get_by_id(item["producto_id"])
                cantidad = item["cantidad"]
                
                if producto.stock_actual < cantidad:
                    raise ValueError(f"Stock insuficiente para {producto.nombre}")
                
                subtotal = producto.precio_unitario * cantidad
                
                # Crear detalle
                detalle = DetalleVenta.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio_unitario,
                    subtotal=subtotal
                )
                detalles.append(detalle)
                
                # Actualizar stock
                producto.stock_actual -= cantidad
                producto.save()
                
                total_venta += subtotal
            
            # Actualizar total de la venta
            venta.total = total_venta
            venta.save()
            
            return venta, detalles

    @log_operacion("gestión_venta")
    def anular_venta(self, venta_id: int) -> bool:
        """Anula una venta y restaura el stock."""
        with db.atomic():
            venta = Venta.get_by_id(venta_id)
            if venta.pagada:
                raise ValueError("No se puede anular una venta pagada")
            
            # Restaurar stock
            for detalle in venta.detalles:
                producto = detalle.producto
                producto.stock_actual += detalle.cantidad
                producto.save()
            
            # Eliminar detalles y venta
            DetalleVenta.delete().where(DetalleVenta.venta == venta).execute()
            venta.delete_instance()
            return True

    # Gestión de Pagos
    @log_operacion("gestión_pago")
    def registrar_pago(self, venta_id: int, monto: float, 
                      metodo_pago: str, notas: Optional[str] = None) -> Pago:
        """
        Registra un pago para una venta.
        
        Args:
            venta_id (int): ID de la venta
            monto (float): Monto del pago
            metodo_pago (str): Método de pago utilizado
            notas (Optional[str]): Notas adicionales
            
        Returns:
            Pago: Instancia del pago creado
        """
        with db.atomic():
            venta = Venta.get_by_id(venta_id)
            
            # Verificar si el monto excede el total pendiente
            pagos_previos = Pago.select(fn.SUM(Pago.monto)).where(Pago.venta == venta).scalar() or 0
            pendiente = float(venta.total) - float(pagos_previos)
            
            if float(monto) > pendiente:
                raise ValueError("El monto del pago excede el total pendiente")
            
            pago = Pago.create(
                venta=venta,
                monto=monto,
                metodo_pago=metodo_pago,
                notas=notas
            )
            
            # Actualizar estado de la venta si está completamente pagada
            if float(pagos_previos) + float(monto) >= float(venta.total):
                venta.pagada = True
                venta.save()
                
            return pago

    @log_operacion("gestión_pago")
    def anular_pago(self, pago_id: int) -> bool:
        """Anula un pago y actualiza el estado de la venta."""
        with db.atomic():
            pago = Pago.get_by_id(pago_id)
            venta = pago.venta
            
            # Actualizar estado de la venta
            venta.pagada = False
            venta.save()
            
            # Eliminar pago
            pago.delete_instance()
            return True

    # Reportes y consultas adicionales
    @log_operacion("consulta")
    def obtener_reporte_ventas_cliente(self, desde: Optional[datetime] = None,
                                     hasta: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Obtiene el reporte de ventas por cliente.
        
        Args:
            desde (Optional[datetime]): Fecha inicial
            hasta (Optional[datetime]): Fecha final
            
        Returns:
            List[Dict[str, Any]]: Lista de datos del reporte
        """
        query = (Cliente
                .select(
                    Cliente.nombre,
                    fn.SUM(Venta.total).alias('total_ventas'),
                    fn.COALESCE(fn.SUM(Pago.monto), 0).alias('total_pagado')
                )
                .join(Venta, JOIN.LEFT_OUTER)
                .join(Pago, JOIN.LEFT_OUTER)
                .where(Cliente.activo == True))
        
        if desde:
            query = query.where(Venta.fecha >= desde)
        if hasta:
            query = query.where(Venta.fecha <= hasta)
        
        query = query.group_by(Cliente)
        
        resultados = []
        for r in query:
            resultados.append({
                'cliente': r.nombre,
                'total_ventas': float(r.total_ventas or 0),
                'total_pagado': float(r.total_pagado or 0),
                'saldo': float((r.total_ventas or 0) - (r.total_pagado or 0))
            })
        
        return resultados

    @log_operacion("consulta")
    def obtener_reporte_productos(self, desde: Optional[datetime] = None,
                                hasta: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Obtiene el reporte de productos más vendidos.
        
        Args:
            desde (Optional[datetime]): Fecha inicial
            hasta (Optional[datetime]): Fecha final
            
        Returns:
            List[Dict[str, Any]]: Lista de datos del reporte
        """
        query = (Producto
                .select(
                    Producto.nombre,
                    fn.SUM(DetalleVenta.cantidad).alias('cantidad'),
                    fn.SUM(DetalleVenta.subtotal).alias('total')
                )
                .join(DetalleVenta)
                .join(Venta)
                .where(Producto.activo == True))
        
        if desde:
            query = query.where(Venta.fecha >= desde)
        if hasta:
            query = query.where(Venta.fecha <= hasta)
        
        query = (query
                .group_by(Producto)
                .order_by(fn.SUM(DetalleVenta.cantidad).desc()))
        
        return [{
            'producto': r.nombre,
            'cantidad': int(r.cantidad or 0),
            'total': float(r.total or 0)
        } for r in query]

    @log_operacion("consulta")
    def obtener_reporte_pagos(self, desde: Optional[datetime] = None,
                            hasta: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Obtiene el reporte de pagos.
        
        Args:
            desde (Optional[datetime]): Fecha inicial
            hasta (Optional[datetime]): Fecha final
            
        Returns:
            List[Dict[str, Any]]: Lista de datos del reporte
        """
        query = (Pago
                .select(Pago, Cliente)
                .join(Venta)
                .join(Cliente)
                .order_by(Pago.fecha.desc()))
        
        if desde:
            query = query.where(Pago.fecha >= desde)
        if hasta:
            query = query.where(Pago.fecha <= hasta)
        
        return [{
            'fecha': p.fecha,
            'cliente': p.venta.cliente.nombre,
            'monto': float(p.monto),
            'metodo_pago': p.metodo_pago
        } for p in query]

    @log_operacion("consulta")
    def obtener_reporte_stock(self) -> List[Dict[str, Any]]:
        """
        Obtiene el reporte de stock actual.
        
        Returns:
            List[Dict[str, Any]]: Lista de datos del reporte
        """
        query = (Producto
                .select()
                .where(Producto.activo == True)
                .order_by(Producto.stock_actual))
        
        return [{
            'producto': p.nombre,
            'stock_actual': p.stock_actual,
            'stock_minimo': p.stock_minimo
        } for p in query]

    @log_operacion("consulta")
    def obtener_todas_ventas(self) -> List[Venta]:
        """
        Obtiene todas las ventas ordenadas por fecha.
        
        Returns:
            List[Venta]: Lista de ventas
        """
        return (Venta
                .select()
                .order_by(Venta.fecha.desc()))

    @log_operacion("consulta")
    def filtrar_ventas(self, cliente_id: Optional[int] = None,
                      pagada: Optional[bool] = None) -> List[Venta]:
        """
        Filtra las ventas según los criterios especificados.
        
        Args:
            cliente_id (Optional[int]): ID del cliente
            pagada (Optional[bool]): Estado de pago
            
        Returns:
            List[Venta]: Lista de ventas filtradas
        """
        query = Venta.select().order_by(Venta.fecha.desc())
        
        if cliente_id is not None:
            query = query.where(Venta.cliente_id == cliente_id)
        if pagada is not None:
            query = query.where(Venta.pagada == pagada)
        
        return query

    @log_operacion("consulta")
    def obtener_venta_por_id(self, venta_id: int) -> Venta:
        """
        Obtiene una venta por su ID.
        
        Args:
            venta_id (int): ID de la venta
            
        Returns:
            Venta: Instancia de la venta
        """
        return Venta.get_by_id(venta_id)

    @log_operacion("consulta")
    def obtener_detalles_venta(self, venta_id: int) -> List[DetalleVenta]:
        """
        Obtiene los detalles de una venta.
        
        Args:
            venta_id (int): ID de la venta
            
        Returns:
            List[DetalleVenta]: Lista de detalles de la venta
        """
        return (DetalleVenta
                .select()
                .where(DetalleVenta.venta_id == venta_id))

    @log_operacion("reporte")
    def generar_grafico_ventas_cliente(self, datos: List[Dict[str, Any]], 
                                     canvas: Any, desde: Optional[datetime] = None,
                                     hasta: Optional[datetime] = None) -> None:
        """
        Genera un gráfico de barras de ventas por cliente.
        
        Args:
            datos (List[Dict[str, Any]]): Datos para el gráfico
            canvas (Any): Canvas donde dibujar el gráfico
            desde (Optional[datetime]): Fecha inicial
            hasta (Optional[datetime]): Fecha final
        """
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Preparar datos
        clientes = [d['cliente'] for d in datos]
        ventas = [d['total_ventas'] for d in datos]
        pagos = [d['total_pagado'] for d in datos]
        
        # Crear gráfico de barras
        x = range(len(clientes))
        width = 0.35
        
        ax.bar([i - width/2 for i in x], ventas, width, label='Ventas', color='#2ecc71')
        ax.bar([i + width/2 for i in x], pagos, width, label='Pagado', color='#3498db')
        
        # Configurar gráfico
        ax.set_ylabel('Monto ($)')
        ax.set_title('Ventas y Pagos por Cliente')
        ax.set_xticks(x)
        ax.set_xticklabels(clientes, rotation=45, ha='right')
        ax.legend()
        
        # Ajustar layout
        plt.tight_layout()
        
        # Mostrar en canvas
        canvas_widget = FigureCanvasTkAgg(fig, master=canvas)
        canvas_widget.draw()
        canvas_widget.get_tk_widget().pack(side='top', fill='both', expand=1)

    @log_operacion("reporte")
    def generar_grafico_productos(self, datos: List[Dict[str, Any]], 
                                canvas: Any, desde: Optional[datetime] = None,
                                hasta: Optional[datetime] = None) -> None:
        """
        Genera un gráfico de barras horizontales de productos más vendidos.
        
        Args:
            datos (List[Dict[str, Any]]): Datos para el gráfico
            canvas (Any): Canvas donde dibujar el gráfico
            desde (Optional[datetime]): Fecha inicial
            hasta (Optional[datetime]): Fecha final
        """
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Preparar datos
        productos = [d['producto'] for d in datos]
        cantidades = [d['cantidad'] for d in datos]
        
        # Crear gráfico de barras horizontales
        ax.barh(productos, cantidades, color='#e74c3c')
        
        # Configurar gráfico
        ax.set_xlabel('Cantidad Vendida')
        ax.set_title('Productos Más Vendidos')
        
        # Ajustar layout
        plt.tight_layout()
        
        # Mostrar en canvas
        canvas_widget = FigureCanvasTkAgg(fig, master=canvas)
        canvas_widget.draw()
        canvas_widget.get_tk_widget().pack(side='top', fill='both', expand=1)

    @log_operacion("reporte")
    def generar_grafico_pagos(self, datos: List[Dict[str, Any]], 
                            canvas: Any, desde: Optional[datetime] = None,
                            hasta: Optional[datetime] = None) -> None:
        """
        Genera un gráfico de torta de métodos de pago.
        
        Args:
            datos (List[Dict[str, Any]]): Datos para el gráfico
            canvas (Any): Canvas donde dibujar el gráfico
            desde (Optional[datetime]): Fecha inicial
            hasta (Optional[datetime]): Fecha final
        """
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from collections import defaultdict
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Preparar datos
        metodos = defaultdict(float)
        for pago in datos:
            metodos[pago['metodo_pago']] += pago['monto']
        
        # Crear gráfico de torta
        ax.pie(metodos.values(), labels=metodos.keys(), autopct='%1.1f%%')
        ax.set_title('Distribución de Métodos de Pago')
        
        # Ajustar layout
        plt.tight_layout()
        
        # Mostrar en canvas
        canvas_widget = FigureCanvasTkAgg(fig, master=canvas)
        canvas_widget.draw()
        canvas_widget.get_tk_widget().pack(side='top', fill='both', expand=1)

    @log_operacion("reporte")
    def generar_grafico_stock(self, datos: List[Dict[str, Any]], canvas: Any) -> None:
        """
        Genera un gráfico de barras comparando stock actual vs mínimo.
        
        Args:
            datos (List[Dict[str, Any]]): Datos para el gráfico
            canvas (Any): Canvas donde dibujar el gráfico
        """
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Preparar datos
        productos = [d['producto'] for d in datos]
        stock_actual = [d['stock_actual'] for d in datos]
        stock_minimo = [d['stock_minimo'] for d in datos]
        
        # Crear gráfico de barras
        x = range(len(productos))
        width = 0.35
        
        ax.bar([i - width/2 for i in x], stock_actual, width, 
               label='Stock Actual', color='#2ecc71')
        ax.bar([i + width/2 for i in x], stock_minimo, width, 
               label='Stock Mínimo', color='#e74c3c')
        
        # Configurar gráfico
        ax.set_ylabel('Cantidad')
        ax.set_title('Stock Actual vs Mínimo')
        ax.set_xticks(x)
        ax.set_xticklabels(productos, rotation=45, ha='right')
        ax.legend()
        
        # Ajustar layout
        plt.tight_layout()
        
        # Mostrar en canvas
        canvas_widget = FigureCanvasTkAgg(fig, master=canvas)
        canvas_widget.draw()
        canvas_widget.get_tk_widget().pack(side='top', fill='both', expand=1)

    @log_operacion("reporte")
    def exportar_reporte(self, tipo_reporte: str, desde: Optional[datetime] = None,
                        hasta: Optional[datetime] = None) -> str:
        """
        Exporta el reporte actual a un archivo Excel.
        
        Args:
            tipo_reporte (str): Tipo de reporte a exportar
            desde (Optional[datetime]): Fecha inicial
            hasta (Optional[datetime]): Fecha final
            
        Returns:
            str: Nombre del archivo generado
        """
        import pandas as pd
        from datetime import datetime
        
        # Obtener datos según el tipo de reporte
        if tipo_reporte == 'Ventas por Cliente':
            datos = self.obtener_reporte_ventas_cliente(desde, hasta)
            df = pd.DataFrame(datos)
        elif tipo_reporte == 'Productos más Vendidos':
            datos = self.obtener_reporte_productos(desde, hasta)
            df = pd.DataFrame(datos)
        elif tipo_reporte == 'Balance de Pagos':
            datos = self.obtener_reporte_pagos(desde, hasta)
            df = pd.DataFrame(datos)
        elif tipo_reporte == 'Stock Actual':
            datos = self.obtener_reporte_stock()
            df = pd.DataFrame(datos)
        else:
            raise ValueError(f"Tipo de reporte no válido: {tipo_reporte}")
        
        # Generar nombre de archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"reporte_{tipo_reporte.lower().replace(' ', '_')}_{timestamp}.xlsx"
        
        # Exportar a Excel
        df.to_excel(nombre_archivo, index=False)
        
        return nombre_archivo

    @log_operacion("consulta")
    def obtener_productos_bajo_stock(self) -> List[Producto]:
        """
        Obtiene la lista de productos con stock bajo.
        
        Returns:
            List[Producto]: Lista de productos con stock bajo
        """
        return (Producto
                .select()
                .where(
                    (Producto.activo == True) &
                    (Producto.stock_actual <= Producto.stock_minimo)
                )
                .order_by(Producto.stock_actual))

    @log_operacion("consulta")
    def obtener_cliente_por_id(self, cliente_id: int) -> Cliente:
        """
        Obtiene un cliente por su ID.
        
        Args:
            cliente_id (int): ID del cliente
            
        Returns:
            Cliente: Instancia del cliente
        """
        return Cliente.get_by_id(cliente_id)

    @log_operacion("consulta")
    def obtener_balance_cliente(self, cliente_id: int) -> Dict[str, float]:
        """
        Obtiene el balance de un cliente.
        
        Args:
            cliente_id (int): ID del cliente
            
        Returns:
            Dict[str, float]: Diccionario con total_ventas, total_pagado y saldo_pendiente
        """
        cliente = Cliente.get_by_id(cliente_id)
        
        total_ventas = (Venta
                       .select(fn.COALESCE(fn.SUM(Venta.total), 0))
                       .where(Venta.cliente == cliente)
                       .scalar()) or 0
        
        total_pagado = (Pago
                       .select(fn.COALESCE(fn.SUM(Pago.monto), 0))
                       .join(Venta)
                       .where(Venta.cliente == cliente)
                       .scalar()) or 0
        
        return {
            "total_ventas": float(total_ventas),
            "total_pagado": float(total_pagado),
            "saldo_pendiente": float(total_ventas - total_pagado)
        }

    @log_operacion("consulta")
    def obtener_producto_por_id(self, producto_id: int):
        """
        Obtiene un producto por su ID.
        
        Args:
            producto_id (int): ID del producto a buscar
            
        Returns:
            Producto: Objeto producto si se encuentra, None si no existe
        """
        try:
            return Producto.get_by_id(producto_id)
        except Producto.DoesNotExist:
            return None 