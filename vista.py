import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict, Any, Optional, List
from datetime import datetime
from decimal import Decimal
from controlador import Controlador

class VistaPrincipal:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sistema de Gestión de Bebidas")
        self.root.geometry("800x600")
        
        # Inicializar controlador
        self.controlador = Controlador()
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Inicializar pestañas
        self.tab_clientes = ttk.Frame(self.notebook)
        self.tab_productos = ttk.Frame(self.notebook)
        self.tab_proveedores = ttk.Frame(self.notebook)
        self.tab_ventas = ttk.Frame(self.notebook)
        self.tab_reportes = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_clientes, text='Clientes')
        self.notebook.add(self.tab_productos, text='Productos')
        self.notebook.add(self.tab_proveedores, text='Proveedores')
        self.notebook.add(self.tab_ventas, text='Ventas')
        self.notebook.add(self.tab_reportes, text='Reportes')
        
        # Inicializar componentes
        self._init_clientes()
        self._init_productos()
        self._init_proveedores()
        self._init_ventas()
        self._init_reportes()
        
        # Cargar datos iniciales
        self.actualizar_lista_clientes()
        self.actualizar_lista_productos()
        self.actualizar_lista_proveedores()

    def _init_clientes(self):
        # Frame para búsqueda
        frame_busqueda = ttk.LabelFrame(self.tab_clientes, text="Buscar Cliente")
        frame_busqueda.pack(fill='x', padx=5, pady=5)
        
        self.entry_buscar_cliente = ttk.Entry(frame_busqueda)
        self.entry_buscar_cliente.pack(side='left', padx=5, pady=5, expand=True, fill='x')
        ttk.Button(frame_busqueda, text="Buscar", command=self.buscar_cliente).pack(side='left', padx=5, pady=5)
        ttk.Button(frame_busqueda, text="Nuevo Cliente", command=self.mostrar_dialogo_cliente).pack(side='left', padx=5, pady=5)
        
        # Frame para lista de clientes
        frame_lista = ttk.LabelFrame(self.tab_clientes, text="Clientes")
        frame_lista.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Treeview para clientes
        columns = ('ID', 'Nombre', 'Teléfono', 'Dirección', 'Email', 'Saldo')
        self.tree_clientes = ttk.Treeview(frame_lista, columns=columns, show='headings')
        
        for col in columns:
            self.tree_clientes.heading(col, text=col)
            self.tree_clientes.column(col, width=100)
        
        self.tree_clientes.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree_clientes.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree_clientes.configure(yscrollcommand=scrollbar.set)

        # Botones de acción
        frame_acciones = ttk.Frame(self.tab_clientes)
        frame_acciones.pack(fill='x', padx=5, pady=5)
        ttk.Button(frame_acciones, text="Editar", command=self.editar_cliente).pack(side='left', padx=5)
        ttk.Button(frame_acciones, text="Eliminar", command=self.eliminar_cliente).pack(side='left', padx=5)

    def mostrar_dialogo_cliente(self, cliente: Optional[Any] = None):
        """Muestra el diálogo para agregar o editar un cliente."""
        def guardar_cliente(datos: Dict[str, Any]):
            try:
                if cliente:
                    self.controlador.actualizar_cliente(cliente.id, **datos)
                    self.mostrar_info("Cliente actualizado exitosamente")
                else:
                    self.controlador.agregar_cliente(**datos)
                    self.mostrar_info("Cliente agregado exitosamente")
                self.actualizar_lista_clientes()
            except Exception as e:
                self.mostrar_error(f"Error al guardar cliente: {str(e)}")
        
        dialogo = DialogoCliente(self.root, guardar_cliente, cliente)
        dialogo.grab_set()  # Hacer el diálogo modal

    def editar_cliente(self):
        """Edita el cliente seleccionado."""
        selected_item = self.tree_clientes.selection()
        if not selected_item:
            self.mostrar_error("Por favor, selecciona un cliente para editar.")
            return
        cliente_id = self.tree_clientes.item(selected_item)['values'][0]
        cliente = self.controlador.obtener_cliente_por_id(cliente_id)
        self.mostrar_dialogo_cliente(cliente)

    def eliminar_cliente(self):
        """Elimina el cliente seleccionado."""
        selected_item = self.tree_clientes.selection()
        if not selected_item:
            self.mostrar_error("Por favor, selecciona un cliente para eliminar.")
            return
        cliente_id = self.tree_clientes.item(selected_item)['values'][0]
        if self.mostrar_confirmacion("¿Estás seguro de que deseas eliminar este cliente?"):
            try:
                self.controlador.eliminar_cliente(cliente_id)
                self.actualizar_lista_clientes()
                self.mostrar_info("Cliente eliminado exitosamente")
            except Exception as e:
                self.mostrar_error(f"Error al eliminar cliente: {str(e)}")

    def actualizar_lista_clientes(self):
        """Actualiza la lista de clientes en el treeview."""
        # Limpiar lista actual
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        # Obtener clientes de la base de datos
        try:
            clientes = self.controlador.obtener_todos_clientes()
            for cliente in clientes:
                balance = self.controlador.obtener_balance_cliente(cliente.id)
                self.tree_clientes.insert('', 'end', values=(
                    cliente.id,
                    cliente.nombre,
                    cliente.telefono,
                    cliente.direccion,
                    cliente.email or '',
                    f"${balance['saldo_pendiente']:.2f}"
                ))
        except Exception as e:
            self.mostrar_error(f"Error al cargar clientes: {str(e)}")

    def buscar_cliente(self):
        """Busca clientes según el texto ingresado."""
        texto = self.entry_buscar_cliente.get().strip()
        if not texto:
            self.actualizar_lista_clientes()
            return
        
        # Limpiar lista actual
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        try:
            clientes = self.controlador.buscar_clientes(texto)
            for cliente in clientes:
                balance = self.controlador.obtener_balance_cliente(cliente.id)
                self.tree_clientes.insert('', 'end', values=(
                    cliente.id,
                    cliente.nombre,
                    cliente.telefono,
                    cliente.direccion,
                    cliente.email or '',
                    f"${balance['saldo_pendiente']:.2f}"
                ))
        except Exception as e:
            self.mostrar_error(f"Error al buscar clientes: {str(e)}")

    def _init_productos(self):
        # Frame para búsqueda y filtros
        frame_superior = ttk.LabelFrame(self.tab_productos, text="Buscar Producto")
        frame_superior.pack(fill='x', padx=5, pady=5)
        
        # Búsqueda
        self.entry_buscar_producto = ttk.Entry(frame_superior)
        self.entry_buscar_producto.pack(side='left', padx=5, pady=5, expand=True, fill='x')
        ttk.Button(frame_superior, text="Buscar", command=self.buscar_producto).pack(side='left', padx=5)
        ttk.Button(frame_superior, text="Nuevo Producto", command=self.mostrar_dialogo_producto).pack(side='left', padx=5)
        
        # Lista de productos
        frame_lista = ttk.LabelFrame(self.tab_productos, text="Productos")
        frame_lista.pack(expand=True, fill='both', padx=5, pady=5)
        
        columns = ('ID', 'Nombre', 'Descripción', 'Stock', 'Stock Mínimo', 'Precio', 'Proveedor')
        self.tree_productos = ttk.Treeview(frame_lista, columns=columns, show='headings')
        
        for col in columns:
            self.tree_productos.heading(col, text=col)
            self.tree_productos.column(col, width=100)
        
        self.tree_productos.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree_productos.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree_productos.configure(yscrollcommand=scrollbar.set)
        
        # Botones de acción
        frame_acciones = ttk.Frame(self.tab_productos)
        frame_acciones.pack(fill='x', padx=5, pady=5)
        ttk.Button(frame_acciones, text="Editar", command=self.editar_producto).pack(side='left', padx=5)
        ttk.Button(frame_acciones, text="Eliminar", command=self.eliminar_producto).pack(side='left', padx=5)
        ttk.Button(frame_acciones, text="Ajustar Stock", command=self.mostrar_dialogo_ajuste_stock).pack(side='left', padx=5)
        
        # Frame para alertas de stock bajo
        frame_alertas = ttk.LabelFrame(self.tab_productos, text="Alertas de Stock Bajo")
        frame_alertas.pack(fill='x', padx=5, pady=5)
        
        self.lista_alertas = tk.Listbox(frame_alertas, height=3)
        self.lista_alertas.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Cargar datos iniciales
        self.actualizar_lista_productos()
        self.actualizar_alertas_stock()

    def mostrar_dialogo_producto(self, producto: Optional[Any] = None):
        """Muestra el diálogo para agregar o editar un producto."""
        def guardar_producto(datos: Dict[str, Any]):
            try:
                if producto:
                    self.controlador.actualizar_producto(producto.id, **datos)
                    self.mostrar_info("Producto actualizado exitosamente")
                else:
                    self.controlador.agregar_producto(**datos)
                    self.mostrar_info("Producto agregado exitosamente")
                self.actualizar_lista_productos()
                self.actualizar_alertas_stock()
            except Exception as e:
                self.mostrar_error(f"Error al guardar producto: {str(e)}")
        
        # Obtener lista de proveedores para el combo
        proveedores = self.controlador.obtener_todos_proveedores()
        proveedores_lista = [f"{p.id} - {p.nombre}" for p in proveedores]
        
        dialogo = DialogoProducto(self.root, guardar_producto, proveedores_lista, producto)
        dialogo.grab_set()

    def editar_producto(self):
        """Edita el producto seleccionado."""
        selected_item = self.tree_productos.selection()
        if not selected_item:
            self.mostrar_error("Por favor, selecciona un producto para editar.")
            return
        producto_id = self.tree_productos.item(selected_item)['values'][0]
        producto = self.controlador.obtener_producto_por_id(producto_id)
        self.mostrar_dialogo_producto(producto)

    def eliminar_producto(self):
        """Elimina el producto seleccionado."""
        selected_item = self.tree_productos.selection()
        if not selected_item:
            self.mostrar_error("Por favor, selecciona un producto para eliminar.")
            return
        producto_id = self.tree_productos.item(selected_item)['values'][0]
        if self.mostrar_confirmacion("¿Estás seguro de que deseas eliminar este producto?"):
            try:
                self.controlador.eliminar_producto(producto_id)
                self.actualizar_lista_productos()
                self.actualizar_alertas_stock()
                self.mostrar_info("Producto eliminado exitosamente")
            except Exception as e:
                self.mostrar_error(f"Error al eliminar producto: {str(e)}")

    def mostrar_dialogo_ajuste_stock(self):
        """Muestra el diálogo para ajustar el stock de un producto."""
        selected_item = self.tree_productos.selection()
        if not selected_item:
            self.mostrar_error("Por favor, selecciona un producto para ajustar el stock.")
            return
        producto_id = self.tree_productos.item(selected_item)['values'][0]
        
        def ajustar_stock(cantidad: int, motivo: str):
            try:
                self.controlador.ajustar_stock(producto_id, cantidad, motivo)
                self.actualizar_lista_productos()
                self.actualizar_alertas_stock()
                self.mostrar_info("Stock ajustado exitosamente")
            except Exception as e:
                self.mostrar_error(f"Error al ajustar stock: {str(e)}")
        
        dialogo = DialogoAjusteStock(self.root, ajustar_stock)
        dialogo.grab_set()

    def actualizar_lista_productos(self):
        """Actualiza la lista de productos en el treeview."""
        # Limpiar lista actual
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        
        try:
            productos = self.controlador.obtener_todos_productos()
            for producto in productos:
                self.tree_productos.insert('', 'end', values=(
                    producto.id,
                    producto.nombre,
                    producto.descripcion or '',
                    producto.stock_actual,
                    producto.stock_minimo,
                    f"${float(producto.precio_unitario):.2f}",
                    producto.proveedor.nombre
                ))
        except Exception as e:
            self.mostrar_error(f"Error al cargar productos: {str(e)}")

    def actualizar_alertas_stock(self):
        """Actualiza la lista de alertas de stock bajo."""
        self.lista_alertas.delete(0, tk.END)
        try:
            productos_bajo_stock = self.controlador.obtener_productos_bajo_stock()
            for producto in productos_bajo_stock:
                self.lista_alertas.insert(tk.END, 
                    f"{producto.nombre}: {producto.stock_actual}/{producto.stock_minimo}")
        except Exception as e:
            self.mostrar_error(f"Error al cargar alertas de stock: {str(e)}")

    def buscar_producto(self):
        """Busca productos según el texto ingresado."""
        texto = self.entry_buscar_producto.get().strip()
        if not texto:
            self.actualizar_lista_productos()
            return
        
        # Limpiar lista actual
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        
        try:
            productos = self.controlador.buscar_productos(texto)
            for producto in productos:
                self.tree_productos.insert('', 'end', values=(
                    producto.id,
                    producto.nombre,
                    producto.descripcion or '',
                    producto.stock_actual,
                    producto.stock_minimo,
                    f"${float(producto.precio_unitario):.2f}",
                    producto.proveedor.nombre
                ))
        except Exception as e:
            self.mostrar_error(f"Error al buscar productos: {str(e)}")

    def _init_proveedores(self):
        """Inicializa la pestaña de proveedores."""
        # Frame para búsqueda
        frame_busqueda = ttk.LabelFrame(self.tab_proveedores, text="Buscar Proveedor")
        frame_busqueda.pack(fill='x', padx=5, pady=5)
        
        self.entry_buscar_proveedor = ttk.Entry(frame_busqueda)
        self.entry_buscar_proveedor.pack(side='left', padx=5, pady=5, expand=True, fill='x')
        ttk.Button(frame_busqueda, text="Buscar", command=self.buscar_proveedor).pack(side='left', padx=5)
        ttk.Button(frame_busqueda, text="Nuevo Proveedor", command=self.mostrar_dialogo_proveedor).pack(side='left', padx=5)
        
        # Frame para lista de proveedores
        frame_lista = ttk.LabelFrame(self.tab_proveedores, text="Proveedores")
        frame_lista.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Treeview para proveedores
        columns = ('ID', 'Nombre', 'Teléfono', 'Email', 'Dirección')
        self.tree_proveedores = ttk.Treeview(frame_lista, columns=columns, show='headings')
        
        for col in columns:
            self.tree_proveedores.heading(col, text=col)
            self.tree_proveedores.column(col, width=100)
        
        self.tree_proveedores.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree_proveedores.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree_proveedores.configure(yscrollcommand=scrollbar.set)
        
        # Botones de acción
        frame_acciones = ttk.Frame(self.tab_proveedores)
        frame_acciones.pack(fill='x', padx=5, pady=5)
        ttk.Button(frame_acciones, text="Editar", command=self.editar_proveedor).pack(side='left', padx=5)
        ttk.Button(frame_acciones, text="Eliminar", command=self.eliminar_proveedor).pack(side='left', padx=5)

    def mostrar_dialogo_proveedor(self, proveedor: Optional[Dict[str, Any]] = None):
        """Muestra el diálogo para agregar o editar un proveedor."""
        def guardar_proveedor(datos: Dict[str, Any]):
            try:
                if proveedor:
                    self.controlador.actualizar_proveedor(proveedor['id'], **datos)
                    self.mostrar_info("Proveedor actualizado exitosamente")
                else:
                    self.controlador.agregar_proveedor(**datos)
                    self.mostrar_info("Proveedor agregado exitosamente")
                self.actualizar_lista_proveedores()
            except Exception as e:
                self.mostrar_error(f"Error al guardar proveedor: {str(e)}")
        
        dialogo = DialogoProveedor(self.root, guardar_proveedor, proveedor)
        dialogo.grab_set()

    def editar_proveedor(self):
        """Edita el proveedor seleccionado."""
        selected_item = self.tree_proveedores.selection()
        if not selected_item:
            self.mostrar_error("Por favor, selecciona un proveedor para editar.")
            return
        proveedor_id = self.tree_proveedores.item(selected_item)['values'][0]
        proveedor = self.controlador.obtener_proveedor_por_id(proveedor_id)
        self.mostrar_dialogo_proveedor(proveedor)

    def eliminar_proveedor(self):
        """Elimina el proveedor seleccionado."""
        selected_item = self.tree_proveedores.selection()
        if not selected_item:
            self.mostrar_error("Por favor, selecciona un proveedor para eliminar.")
            return
        proveedor_id = self.tree_proveedores.item(selected_item)['values'][0]
        if self.mostrar_confirmacion("¿Estás seguro de que deseas eliminar este proveedor?"):
            try:
                self.controlador.eliminar_proveedor(proveedor_id)
                self.actualizar_lista_proveedores()
                self.mostrar_info("Proveedor eliminado exitosamente")
            except Exception as e:
                self.mostrar_error(f"Error al eliminar proveedor: {str(e)}")

    def actualizar_lista_proveedores(self):
        """Actualiza la lista de proveedores en el treeview."""
        # Limpiar lista actual
        for item in self.tree_proveedores.get_children():
            self.tree_proveedores.delete(item)
        
        try:
            proveedores = self.controlador.obtener_todos_proveedores()
            for proveedor in proveedores:
                self.tree_proveedores.insert('', 'end', values=(
                    proveedor.id,
                    proveedor.nombre,
                    proveedor.telefono,
                    proveedor.email or '',
                    proveedor.direccion or ''
                ))
        except Exception as e:
            self.mostrar_error(f"Error al cargar proveedores: {str(e)}")

    def buscar_proveedor(self):
        """Busca proveedores según el texto ingresado."""
        texto = self.entry_buscar_proveedor.get().strip()
        if not texto:
            self.actualizar_lista_proveedores()
            return
        
        # Limpiar lista actual
        for item in self.tree_proveedores.get_children():
            self.tree_proveedores.delete(item)
        
        try:
            proveedores = self.controlador.buscar_proveedores(texto)
            for proveedor in proveedores:
                self.tree_proveedores.insert('', 'end', values=(
                    proveedor.id,
                    proveedor.nombre,
                    proveedor.telefono,
                    proveedor.email or '',
                    proveedor.direccion or ''
                ))
        except Exception as e:
            self.mostrar_error(f"Error al buscar proveedores: {str(e)}")

    def _init_ventas(self):
        """Inicializa la pestaña de ventas."""
        # Frame superior para nueva venta
        frame_nueva_venta = ttk.LabelFrame(self.tab_ventas, text="Nueva Venta")
        frame_nueva_venta.pack(fill='x', padx=5, pady=5)
        
        # Cliente
        frame_cliente = ttk.Frame(frame_nueva_venta)
        frame_cliente.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(frame_cliente, text="Cliente:").pack(side='left', padx=5)
        self.combo_cliente = ttk.Combobox(frame_cliente, width=50)
        self.combo_cliente.pack(side='left', padx=5, expand=True, fill='x')
        
        # Productos
        frame_productos = ttk.Frame(frame_nueva_venta)
        frame_productos.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(frame_productos, text="Producto:").pack(side='left', padx=5)
        self.combo_producto = ttk.Combobox(frame_productos, width=50)
        self.combo_producto.pack(side='left', padx=5, expand=True, fill='x')
        
        ttk.Label(frame_productos, text="Cantidad:").pack(side='left', padx=5)
        self.spinbox_cantidad = ttk.Spinbox(frame_productos, from_=1, to=1000, width=10)
        self.spinbox_cantidad.pack(side='left', padx=5)
        
        ttk.Button(frame_productos, text="Agregar", command=self.agregar_item_venta).pack(side='left', padx=5)
        
        # Lista de items
        frame_items = ttk.LabelFrame(frame_nueva_venta, text="Items de la Venta")
        frame_items.pack(fill='both', expand=True, padx=5, pady=5)
        
        columns = ('Producto', 'Cantidad', 'Precio Unit.', 'Subtotal')
        self.tree_items = ttk.Treeview(frame_items, columns=columns, show='headings', height=5)
        
        for col in columns:
            self.tree_items.heading(col, text=col)
            self.tree_items.column(col, width=100)
        
        self.tree_items.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Total y botón finalizar
        frame_total = ttk.Frame(frame_nueva_venta)
        frame_total.pack(fill='x', padx=5, pady=5)
        
        self.label_total = ttk.Label(frame_total, text="Total: $0.00", font=('Arial', 12, 'bold'))
        self.label_total.pack(side='left', padx=5)
        ttk.Button(frame_total, text="Finalizar Venta", command=self.finalizar_venta).pack(side='right', padx=5)
        ttk.Button(frame_total, text="Cancelar Venta", command=self.cancelar_venta).pack(side='right', padx=5)
        
        # Historial de ventas
        frame_historial = ttk.LabelFrame(self.tab_ventas, text="Historial de Ventas")
        frame_historial.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Filtros
        frame_filtros = ttk.Frame(frame_historial)
        frame_filtros.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(frame_filtros, text="Cliente:").pack(side='left', padx=5)
        self.combo_filtro_cliente = ttk.Combobox(frame_filtros)
        self.combo_filtro_cliente.pack(side='left', padx=5)
        
        ttk.Label(frame_filtros, text="Estado:").pack(side='left', padx=5)
        self.combo_filtro_estado = ttk.Combobox(frame_filtros, values=['Todas', 'Pagadas', 'Pendientes'])
        self.combo_filtro_estado.set('Todas')
        self.combo_filtro_estado.pack(side='left', padx=5)
        
        ttk.Button(frame_filtros, text="Filtrar", command=self.filtrar_ventas).pack(side='left', padx=5)
        
        # Lista de ventas
        columns = ('ID', 'Fecha', 'Cliente', 'Total', 'Estado')
        self.tree_ventas = ttk.Treeview(frame_historial, columns=columns, show='headings')
        
        for col in columns:
            self.tree_ventas.heading(col, text=col)
            self.tree_ventas.column(col, width=100)
        
        self.tree_ventas.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Botones de acción
        frame_acciones = ttk.Frame(frame_historial)
        frame_acciones.pack(fill='x', padx=5, pady=5)
        ttk.Button(frame_acciones, text="Ver Detalles", command=self.ver_detalles_venta).pack(side='left', padx=5)
        ttk.Button(frame_acciones, text="Registrar Pago", command=self.mostrar_dialogo_pago).pack(side='left', padx=5)
        ttk.Button(frame_acciones, text="Anular Venta", command=self.anular_venta).pack(side='left', padx=5)
        
        # Inicializar datos
        self.items_venta = []
        self.total_venta = 0
        self.actualizar_combos()
        self.actualizar_historial_ventas()

    def actualizar_combos(self):
        """Actualiza los combobox con los datos actuales."""
        try:
            # Actualizar combo de clientes
            clientes = self.controlador.obtener_todos_clientes()
            clientes_valores = [f"{c.id} - {c.nombre}" for c in clientes]
            self.combo_cliente['values'] = clientes_valores
            self.combo_filtro_cliente['values'] = ['Todos'] + clientes_valores
            self.combo_filtro_cliente.set('Todos')
            
            # Actualizar combo de productos
            productos = self.controlador.obtener_todos_productos()
            productos_valores = []
            for p in productos:
                if p.stock_actual > 0:  # Solo mostrar productos con stock disponible
                    productos_valores.append(
                        f"{p.id} - {p.nombre} (Stock: {p.stock_actual}) ${float(p.precio_unitario):.2f}"
                    )
            self.combo_producto['values'] = productos_valores
            
        except Exception as e:
            self.mostrar_error(f"Error al cargar datos en los combos: {str(e)}")

    def agregar_item_venta(self):
        """Agrega un item a la venta actual."""
        if not self.combo_producto.get():
            self.mostrar_error("Debe seleccionar un producto")
            return
        
        try:
            cantidad = int(self.spinbox_cantidad.get())
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")
        except ValueError:
            self.mostrar_error("La cantidad debe ser un número entero positivo")
            return
        
        try:
            producto_id = int(self.combo_producto.get().split(' - ')[0])
            producto = self.controlador.obtener_producto_por_id(producto_id)
            
            if producto.stock_actual < cantidad:
                self.mostrar_error(f"Stock insuficiente. Disponible: {producto.stock_actual}")
                return
            
            subtotal = float(producto.precio_unitario) * cantidad
            
            # Agregar a la lista visual
            self.tree_items.insert('', 'end', values=(
                producto.nombre,
                cantidad,
                f"${float(producto.precio_unitario):.2f}",
                f"${subtotal:.2f}"
            ))
            
            # Agregar a la lista interna
            self.items_venta.append({
                "producto_id": producto_id,
                "cantidad": cantidad,
                "precio_unitario": float(producto.precio_unitario),
                "subtotal": subtotal
            })
            
            # Actualizar total
            self.total_venta += subtotal
            self.label_total.config(text=f"Total: ${self.total_venta:.2f}")
            
            # Limpiar selección
            self.combo_producto.set('')
            self.spinbox_cantidad.set(1)
            
        except Exception as e:
            self.mostrar_error(f"Error al agregar item: {str(e)}")

    def finalizar_venta(self):
        """Finaliza la venta actual."""
        if not self.items_venta:
            self.mostrar_error("Debe agregar al menos un producto")
            return
        
        if not self.combo_cliente.get():
            self.mostrar_error("Debe seleccionar un cliente")
            return
        
        try:
            cliente_id = int(self.combo_cliente.get().split(' - ')[0])
            
            # Registrar venta
            venta, detalles = self.controlador.registrar_venta(
                cliente_id=cliente_id,
                items=[{"producto_id": item["producto_id"], "cantidad": item["cantidad"]}
                      for item in self.items_venta]
            )
            
            self.mostrar_info("Venta registrada exitosamente")
            self.cancelar_venta()  # Limpiar formulario
            self.actualizar_historial_ventas()
            
        except Exception as e:
            self.mostrar_error(f"Error al finalizar venta: {str(e)}")

    def cancelar_venta(self):
        """Cancela la venta actual."""
        self.combo_cliente.set('')
        self.combo_producto.set('')
        self.spinbox_cantidad.set(1)
        for item in self.tree_items.get_children():
            self.tree_items.delete(item)
        self.items_venta = []
        self.total_venta = 0
        self.label_total.config(text="Total: $0.00")

    def actualizar_historial_ventas(self):
        """Actualiza la lista de ventas en el historial."""
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)
        
        try:
            ventas = self.controlador.obtener_todas_ventas()
            for venta in ventas:
                self.tree_ventas.insert('', 'end', values=(
                    venta.id,
                    venta.fecha.strftime("%Y-%m-%d %H:%M"),
                    venta.cliente.nombre,
                    f"${float(venta.total):.2f}",
                    "Pagada" if venta.pagada else "Pendiente"
                ))
        except Exception as e:
            self.mostrar_error(f"Error al cargar historial: {str(e)}")

    def filtrar_ventas(self):
        """Filtra las ventas según los criterios seleccionados."""
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)
        
        try:
            # Obtener filtros
            cliente = self.combo_filtro_cliente.get()
            cliente_id = int(cliente.split(' - ')[0]) if cliente != 'Todos' else None
            
            estado = self.combo_filtro_estado.get()
            pagada = None
            if estado == 'Pagadas':
                pagada = True
            elif estado == 'Pendientes':
                pagada = False
            
            # Aplicar filtros
            ventas = self.controlador.filtrar_ventas(cliente_id=cliente_id, pagada=pagada)
            
            for venta in ventas:
                self.tree_ventas.insert('', 'end', values=(
                    venta.id,
                    venta.fecha.strftime("%Y-%m-%d %H:%M"),
                    venta.cliente.nombre,
                    f"${float(venta.total):.2f}",
                    "Pagada" if venta.pagada else "Pendiente"
                ))
        except Exception as e:
            self.mostrar_error(f"Error al filtrar ventas: {str(e)}")

    def ver_detalles_venta(self):
        """Muestra los detalles de la venta seleccionada."""
        selected_item = self.tree_ventas.selection()
        if not selected_item:
            self.mostrar_error("Por favor, selecciona una venta para ver sus detalles.")
            return
        
        venta_id = self.tree_ventas.item(selected_item)['values'][0]
        try:
            venta = self.controlador.obtener_venta_por_id(venta_id)
            detalles = self.controlador.obtener_detalles_venta(venta_id)
            
            dialogo = DialogoDetallesVenta(self.root, venta, detalles)
            dialogo.grab_set()
        except Exception as e:
            self.mostrar_error(f"Error al cargar detalles: {str(e)}")

    def mostrar_dialogo_pago(self):
        """Muestra el diálogo para registrar un pago."""
        selected_item = self.tree_ventas.selection()
        if not selected_item:
            self.mostrar_error("Por favor, selecciona una venta para registrar el pago.")
            return
        
        venta_id = self.tree_ventas.item(selected_item)['values'][0]
        try:
            venta = self.controlador.obtener_venta_por_id(venta_id)
            if venta.pagada:
                self.mostrar_error("Esta venta ya está pagada")
                return
            
            def registrar_pago(datos: Dict[str, Any]):
                try:
                    self.controlador.registrar_pago(
                        venta_id=venta_id,
                        monto=datos['monto'],
                        metodo_pago=datos['metodo_pago'],
                        notas=datos.get('notas')
                    )
                    self.mostrar_info("Pago registrado exitosamente")
                    self.actualizar_historial_ventas()
                except Exception as e:
                    self.mostrar_error(f"Error al registrar pago: {str(e)}")
            
            dialogo = DialogoPago(self.root, registrar_pago, float(venta.total))
            dialogo.grab_set()
        except Exception as e:
            self.mostrar_error(f"Error al cargar venta: {str(e)}")

    def anular_venta(self):
        """Anula la venta seleccionada."""
        selected_item = self.tree_ventas.selection()
        if not selected_item:
            self.mostrar_error("Por favor, selecciona una venta para anular.")
            return
        
        venta_id = self.tree_ventas.item(selected_item)['values'][0]
        if self.mostrar_confirmacion("¿Estás seguro de que deseas anular esta venta?"):
            try:
                self.controlador.anular_venta(venta_id)
                self.actualizar_historial_ventas()
                self.mostrar_info("Venta anulada exitosamente")
            except Exception as e:
                self.mostrar_error(f"Error al anular venta: {str(e)}")

    def _init_reportes(self):
        """Inicializa la pestaña de reportes."""
        # Frame para filtros
        frame_filtros = ttk.LabelFrame(self.tab_reportes, text="Filtros")
        frame_filtros.pack(fill='x', padx=5, pady=5)
        
        # Período
        frame_periodo = ttk.Frame(frame_filtros)
        frame_periodo.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(frame_periodo, text="Desde:").pack(side='left', padx=5)
        self.fecha_desde = ttk.Entry(frame_periodo)
        self.fecha_desde.pack(side='left', padx=5)
        ttk.Label(frame_periodo, text="Hasta:").pack(side='left', padx=5)
        self.fecha_hasta = ttk.Entry(frame_periodo)
        self.fecha_hasta.pack(side='left', padx=5)
        
        # Tipo de reporte
        frame_tipo = ttk.Frame(frame_filtros)
        frame_tipo.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(frame_tipo, text="Tipo de Reporte:").pack(side='left', padx=5)
        self.combo_reporte = ttk.Combobox(frame_tipo, values=[
            'Ventas por Cliente',
            'Productos más Vendidos',
            'Balance de Pagos',
            'Stock Actual'
        ])
        self.combo_reporte.pack(side='left', padx=5, expand=True, fill='x')
        self.combo_reporte.set('Ventas por Cliente')
        
        ttk.Button(frame_tipo, text="Generar", command=self.generar_reporte).pack(side='left', padx=5)
        
        # Frame para gráfico
        frame_grafico = ttk.LabelFrame(self.tab_reportes, text="Visualización")
        frame_grafico.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Canvas para el gráfico
        self.canvas_grafico = tk.Canvas(frame_grafico, bg='white')
        self.canvas_grafico.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Frame para datos
        self.frame_datos = ttk.LabelFrame(self.tab_reportes, text="Datos")
        self.frame_datos.pack(fill='x', padx=5, pady=5)
        
        # Treeview para datos
        self.tree_datos = ttk.Treeview(self.frame_datos, show='headings', height=5)
        self.tree_datos.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Botón para exportar
        ttk.Button(self.tab_reportes, text="Exportar a Excel", 
                  command=self.exportar_reporte).pack(pady=5)

    def generar_reporte(self):
        """Genera el reporte seleccionado."""
        tipo_reporte = self.combo_reporte.get()
        
        try:
            # Obtener fechas si están especificadas
            desde = None
            hasta = None
            if self.fecha_desde.get().strip():
                desde = datetime.strptime(self.fecha_desde.get().strip(), "%Y-%m-%d")
            if self.fecha_hasta.get().strip():
                hasta = datetime.strptime(self.fecha_hasta.get().strip(), "%Y-%m-%d")
            
            # Generar reporte según el tipo
            if tipo_reporte == 'Ventas por Cliente':
                self._generar_reporte_ventas_cliente(desde, hasta)
            elif tipo_reporte == 'Productos más Vendidos':
                self._generar_reporte_productos(desde, hasta)
            elif tipo_reporte == 'Balance de Pagos':
                self._generar_reporte_pagos(desde, hasta)
            elif tipo_reporte == 'Stock Actual':
                self._generar_reporte_stock()
            
        except ValueError:
            self.mostrar_error("Formato de fecha inválido. Use YYYY-MM-DD")
        except Exception as e:
            self.mostrar_error(f"Error al generar reporte: {str(e)}")

    def _generar_reporte_ventas_cliente(self, desde: Optional[datetime], hasta: Optional[datetime]):
        """Genera el reporte de ventas por cliente."""
        # Obtener datos
        datos = self.controlador.obtener_reporte_ventas_cliente(desde, hasta)
        
        # Configurar treeview
        self.tree_datos['columns'] = ('Cliente', 'Total Ventas', 'Total Pagado', 'Saldo')
        for col in self.tree_datos['columns']:
            self.tree_datos.heading(col, text=col)
            self.tree_datos.column(col, width=100)
        
        # Limpiar datos anteriores
        for item in self.tree_datos.get_children():
            self.tree_datos.delete(item)
        
        # Insertar nuevos datos
        for dato in datos:
            self.tree_datos.insert('', 'end', values=(
                dato['cliente'],
                f"${dato['total_ventas']:.2f}",
                f"${dato['total_pagado']:.2f}",
                f"${dato['saldo']:.2f}"
            ))
        
        # Generar gráfico
        self.controlador.generar_grafico_ventas_cliente(
            datos, self.canvas_grafico, desde, hasta)

    def _generar_reporte_productos(self, desde: Optional[datetime], hasta: Optional[datetime]):
        """Genera el reporte de productos más vendidos."""
        # Obtener datos
        datos = self.controlador.obtener_reporte_productos(desde, hasta)
        
        # Configurar treeview
        self.tree_datos['columns'] = ('Producto', 'Cantidad Vendida', 'Total Ventas')
        for col in self.tree_datos['columns']:
            self.tree_datos.heading(col, text=col)
            self.tree_datos.column(col, width=100)
        
        # Limpiar datos anteriores
        for item in self.tree_datos.get_children():
            self.tree_datos.delete(item)
        
        # Insertar nuevos datos
        for dato in datos:
            self.tree_datos.insert('', 'end', values=(
                dato['producto'],
                dato['cantidad'],
                f"${dato['total']:.2f}"
            ))
        
        # Generar gráfico
        self.controlador.generar_grafico_productos(
            datos, self.canvas_grafico, desde, hasta)

    def _generar_reporte_pagos(self, desde: Optional[datetime], hasta: Optional[datetime]):
        """Genera el reporte de balance de pagos."""
        # Obtener datos
        datos = self.controlador.obtener_reporte_pagos(desde, hasta)
        
        # Configurar treeview
        self.tree_datos['columns'] = ('Fecha', 'Cliente', 'Monto', 'Método')
        for col in self.tree_datos['columns']:
            self.tree_datos.heading(col, text=col)
            self.tree_datos.column(col, width=100)
        
        # Limpiar datos anteriores
        for item in self.tree_datos.get_children():
            self.tree_datos.delete(item)
        
        # Insertar nuevos datos
        for dato in datos:
            self.tree_datos.insert('', 'end', values=(
                dato['fecha'].strftime("%Y-%m-%d"),
                dato['cliente'],
                f"${dato['monto']:.2f}",
                dato['metodo_pago']
            ))
        
        # Generar gráfico
        self.controlador.generar_grafico_pagos(
            datos, self.canvas_grafico, desde, hasta)

    def _generar_reporte_stock(self):
        """Genera el reporte de stock actual."""
        # Obtener datos
        datos = self.controlador.obtener_reporte_stock()
        
        # Configurar treeview
        self.tree_datos['columns'] = ('Producto', 'Stock Actual', 'Stock Mínimo', 'Estado')
        for col in self.tree_datos['columns']:
            self.tree_datos.heading(col, text=col)
            self.tree_datos.column(col, width=100)
        
        # Limpiar datos anteriores
        for item in self.tree_datos.get_children():
            self.tree_datos.delete(item)
        
        # Insertar nuevos datos
        for dato in datos:
            estado = "Normal"
            if dato['stock_actual'] <= dato['stock_minimo']:
                estado = "Bajo"
            elif dato['stock_actual'] == 0:
                estado = "Agotado"
            
            self.tree_datos.insert('', 'end', values=(
                dato['producto'],
                dato['stock_actual'],
                dato['stock_minimo'],
                estado
            ))
        
        # Generar gráfico
        self.controlador.generar_grafico_stock(datos, self.canvas_grafico)

    def exportar_reporte(self):
        """Exporta el reporte actual a Excel."""
        tipo_reporte = self.combo_reporte.get()
        try:
            # Obtener fechas si están especificadas
            desde = None
            hasta = None
            if self.fecha_desde.get().strip():
                desde = datetime.strptime(self.fecha_desde.get().strip(), "%Y-%m-%d")
            if self.fecha_hasta.get().strip():
                hasta = datetime.strptime(self.fecha_hasta.get().strip(), "%Y-%m-%d")
            
            # Exportar según el tipo
            nombre_archivo = self.controlador.exportar_reporte(
                tipo_reporte, desde, hasta)
            
            self.mostrar_info(f"Reporte exportado exitosamente: {nombre_archivo}")
            
        except ValueError:
            self.mostrar_error("Formato de fecha inválido. Use YYYY-MM-DD")
        except Exception as e:
            self.mostrar_error(f"Error al exportar reporte: {str(e)}")

    def mostrar_error(self, mensaje: str):
        """Muestra un mensaje de error."""
        messagebox.showerror("Error", mensaje)

    def mostrar_info(self, mensaje: str):
        """Muestra un mensaje informativo."""
        messagebox.showinfo("Información", mensaje)

    def mostrar_confirmacion(self, mensaje: str) -> bool:
        """Muestra un diálogo de confirmación."""
        return messagebox.askyesno("Confirmación", mensaje)

class DialogoCliente(tk.Toplevel):
    def __init__(self, parent, callback_guardar: Callable[[Dict[str, Any]], None], cliente: Optional[Any] = None):
        super().__init__(parent)
        self.title("Cliente")
        self.callback_guardar = callback_guardar
        
        # Campos
        ttk.Label(self, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre = ttk.Entry(self)
        self.nombre.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Teléfono:").grid(row=1, column=0, padx=5, pady=5)
        self.telefono = ttk.Entry(self)
        self.telefono.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        self.email = ttk.Entry(self)
        self.email.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Dirección:").grid(row=3, column=0, padx=5, pady=5)
        self.direccion = ttk.Entry(self)
        self.direccion.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Límite de Crédito:").grid(row=4, column=0, padx=5, pady=5)
        self.limite_credito = ttk.Entry(self)
        self.limite_credito.grid(row=4, column=1, padx=5, pady=5)
        
        # Botones
        frame_botones = ttk.Frame(self)
        frame_botones.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(frame_botones, text="Guardar", command=self._guardar).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=self.destroy).pack(side='left', padx=5)

        # Si se está editando un cliente, cargar los datos
        if cliente:
            self.nombre.insert(0, cliente.nombre)
            self.telefono.insert(0, cliente.telefono)
            self.email.insert(0, cliente.email or '')
            self.direccion.insert(0, cliente.direccion)
            self.limite_credito.insert(0, str(cliente.limite_credito))

    def _guardar(self):
        """Recopila los datos del formulario y llama al callback de guardado."""
        try:
            limite_credito = float(self.limite_credito.get() or 0)
        except ValueError:
            messagebox.showerror("Error", "El límite de crédito debe ser un número")
            return
        
        datos = {
            "nombre": self.nombre.get(),
            "telefono": self.telefono.get(),
            "email": self.email.get(),
            "direccion": self.direccion.get(),
            "limite_credito": limite_credito
        }
        
        self.callback_guardar(datos)
        self.destroy()

class DialogoAjusteStock(tk.Toplevel):
    def __init__(self, parent, callback_ajustar: Callable[[int, str], None]):
        super().__init__(parent)
        self.title("Ajustar Stock")
        self.callback_ajustar = callback_ajustar
        
        # Campos
        ttk.Label(self, text="Cantidad (+/-):").grid(row=0, column=0, padx=5, pady=5)
        self.cantidad = ttk.Entry(self)
        self.cantidad.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Motivo:").grid(row=1, column=0, padx=5, pady=5)
        self.motivo = ttk.Entry(self)
        self.motivo.grid(row=1, column=1, padx=5, pady=5)
        
        # Botones
        frame_botones = ttk.Frame(self)
        frame_botones.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(frame_botones, text="Guardar", command=self._guardar).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=self.destroy).pack(side='left', padx=5)

    def _guardar(self):
        """Recopila los datos del formulario y llama al callback de ajuste."""
        try:
            cantidad = int(self.cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero")
            return
        
        motivo = self.motivo.get().strip()
        if not motivo:
            messagebox.showerror("Error", "Debe ingresar un motivo para el ajuste")
            return
        
        self.callback_ajustar(cantidad, motivo)
        self.destroy()

class DialogoProducto(tk.Toplevel):
    def __init__(self, parent, callback_guardar: Callable[[Dict[str, Any]], None],
                 proveedores: list, producto: Optional[Any] = None):
        super().__init__(parent)
        self.title("Producto")
        self.callback_guardar = callback_guardar
        
        # Campos
        ttk.Label(self, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre = ttk.Entry(self)
        self.nombre.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Descripción:").grid(row=1, column=0, padx=5, pady=5)
        self.descripcion = ttk.Entry(self)
        self.descripcion.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Precio:").grid(row=2, column=0, padx=5, pady=5)
        self.precio = ttk.Entry(self)
        self.precio.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Stock Inicial:").grid(row=3, column=0, padx=5, pady=5)
        self.stock = ttk.Entry(self)
        self.stock.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Stock Mínimo:").grid(row=4, column=0, padx=5, pady=5)
        self.stock_minimo = ttk.Entry(self)
        self.stock_minimo.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Proveedor:").grid(row=5, column=0, padx=5, pady=5)
        self.proveedor = ttk.Combobox(self, values=proveedores)
        self.proveedor.grid(row=5, column=1, padx=5, pady=5)
        
        # Botones
        frame_botones = ttk.Frame(self)
        frame_botones.grid(row=6, column=0, columnspan=2, pady=10)
        
        ttk.Button(frame_botones, text="Guardar", command=self._guardar).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=self.destroy).pack(side='left', padx=5)

        # Si se está editando un producto, cargar los datos
        if producto:
            self.nombre.insert(0, producto.nombre)
            self.descripcion.insert(0, producto.descripcion or '')
            self.precio.insert(0, str(producto.precio_unitario))
            self.stock.insert(0, str(producto.stock_actual))
            self.stock_minimo.insert(0, str(producto.stock_minimo))
            # Seleccionar el proveedor correcto en el combo
            for i, prov in enumerate(proveedores):
                if str(producto.proveedor_id) in prov:
                    self.proveedor.current(i)
                    break

    def _guardar(self):
        """Recopila los datos del formulario y llama al callback de guardado."""
        try:
            precio = float(self.precio.get())
            stock = int(self.stock.get())
            stock_minimo = int(self.stock_minimo.get() or 10)
        except ValueError:
            messagebox.showerror("Error", "Los valores numéricos son inválidos")
            return
        
        if not self.proveedor.get():
            messagebox.showerror("Error", "Debe seleccionar un proveedor")
            return
        
        proveedor_id = int(self.proveedor.get().split(' - ')[0])
        
        datos = {
            "nombre": self.nombre.get(),
            "descripcion": self.descripcion.get(),
            "precio": precio,
            "stock": stock,
            "stock_minimo": stock_minimo,
            "proveedor_id": proveedor_id
        }
        
        self.callback_guardar(datos)
        self.destroy()

class DialogoProveedor(tk.Toplevel):
    def __init__(self, parent, callback_guardar: Callable[[Dict[str, Any]], None],
                 proveedor: Optional[Dict[str, Any]] = None):
        super().__init__(parent)
        self.title("Proveedor")
        self.callback_guardar = callback_guardar
        
        # Campos
        ttk.Label(self, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre = ttk.Entry(self)
        self.nombre.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Teléfono:").grid(row=1, column=0, padx=5, pady=5)
        self.telefono = ttk.Entry(self)
        self.telefono.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        self.email = ttk.Entry(self)
        self.email.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Dirección:").grid(row=3, column=0, padx=5, pady=5)
        self.direccion = ttk.Entry(self)
        self.direccion.grid(row=3, column=1, padx=5, pady=5)
        
        # Botones
        frame_botones = ttk.Frame(self)
        frame_botones.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(frame_botones, text="Guardar", command=self._guardar).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=self.destroy).pack(side='left', padx=5)

        # Si se está editando un proveedor, cargar los datos
        if proveedor:
            self.nombre.insert(0, proveedor['nombre'])
            self.telefono.insert(0, proveedor['telefono'])
            self.email.insert(0, proveedor['email'] or '')
            self.direccion.insert(0, proveedor['direccion'] or '')

    def _guardar(self):
        """Recopila los datos del formulario y llama al callback de guardado."""
        datos = {
            "nombre": self.nombre.get(),
            "telefono": self.telefono.get(),
            "email": self.email.get() or None,
            "direccion": self.direccion.get() or None
        }
        
        self.callback_guardar(datos)
        self.destroy()

class DialogoDetallesVenta(tk.Toplevel):
    def __init__(self, parent, venta: Any, detalles: List[Any]):
        super().__init__(parent)
        self.title(f"Detalles de Venta #{venta.id}")
        self.geometry("600x400")
        
        # Información de la venta
        frame_info = ttk.LabelFrame(self, text="Información de la Venta")
        frame_info.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(frame_info, text=f"Cliente: {venta.cliente.nombre}").pack(padx=5, pady=2)
        ttk.Label(frame_info, text=f"Fecha: {venta.fecha.strftime('%Y-%m-%d %H:%M')}").pack(padx=5, pady=2)
        ttk.Label(frame_info, text=f"Estado: {'Pagada' if venta.pagada else 'Pendiente'}").pack(padx=5, pady=2)
        
        # Detalles
        frame_detalles = ttk.LabelFrame(self, text="Items")
        frame_detalles.pack(fill='both', expand=True, padx=5, pady=5)
        
        columns = ('Producto', 'Cantidad', 'Precio Unit.', 'Subtotal')
        tree = ttk.Treeview(frame_detalles, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        for detalle in detalles:
            tree.insert('', 'end', values=(
                detalle.producto.nombre,
                detalle.cantidad,
                f"${float(detalle.precio_unitario):.2f}",
                f"${float(detalle.subtotal):.2f}"
            ))
        
        tree.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Total
        ttk.Label(self, text=f"Total: ${float(venta.total):.2f}",
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Botón cerrar
        ttk.Button(self, text="Cerrar", command=self.destroy).pack(pady=5)

class DialogoPago(tk.Toplevel):
    def __init__(self, parent, callback_guardar: Callable[[Dict[str, Any]], None], total: float):
        super().__init__(parent)
        self.title("Registrar Pago")
        self.callback_guardar = callback_guardar
        
        ttk.Label(self, text=f"Total a pagar: ${total:.2f}",
                 font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Campos
        ttk.Label(self, text="Monto:").grid(row=1, column=0, padx=5, pady=5)
        self.monto = ttk.Entry(self)
        self.monto.grid(row=1, column=1, padx=5, pady=5)
        self.monto.insert(0, str(total))
        
        ttk.Label(self, text="Método de Pago:").grid(row=2, column=0, padx=5, pady=5)
        self.metodo_pago = ttk.Combobox(self, values=['Efectivo', 'Tarjeta', 'Transferencia'])
        self.metodo_pago.grid(row=2, column=1, padx=5, pady=5)
        self.metodo_pago.set('Efectivo')
        
        ttk.Label(self, text="Notas:").grid(row=3, column=0, padx=5, pady=5)
        self.notas = ttk.Entry(self)
        self.notas.grid(row=3, column=1, padx=5, pady=5)
        
        # Botones
        frame_botones = ttk.Frame(self)
        frame_botones.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(frame_botones, text="Guardar", command=self._guardar).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=self.destroy).pack(side='left', padx=5)

    def _guardar(self):
        """Recopila los datos del formulario y llama al callback de guardado."""
        try:
            monto = float(self.monto.get())
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número")
            return
        
        if not self.metodo_pago.get():
            messagebox.showerror("Error", "Debe seleccionar un método de pago")
            return
        
        datos = {
            "monto": monto,
            "metodo_pago": self.metodo_pago.get(),
            "notas": self.notas.get() or None
        }
        
        self.callback_guardar(datos)
        self.destroy() 