# Manual de Usuario - Sistema de Gestión de Bebidas

## Índice
1. [Introducción](#introducción)
2. [Inicio del Sistema](#inicio-del-sistema)
3. [Gestión de Clientes](#gestión-de-clientes)
4. [Gestión de Productos](#gestión-de-productos)
5. [Gestión de Proveedores](#gestión-de-proveedores)
6. [Gestión de Ventas](#gestión-de-ventas)
7. [Reportes](#reportes)

## Introducción

El Sistema de Gestión de Bebidas es una aplicación diseñada para administrar el inventario, ventas y clientes de su negocio de distribución de bebidas. Este manual le guiará a través de todas las funcionalidades disponibles.

## Inicio del Sistema

Para iniciar el sistema:
1. Abra una terminal en la carpeta del proyecto
2. Ejecute el comando: `python main.py`
3. Se abrirá la ventana principal con cinco pestañas:
   - Clientes
   - Productos
   - Proveedores
   - Ventas
   - Reportes

## Gestión de Clientes

### Agregar un Nuevo Cliente
1. En la pestaña "Clientes", haga clic en "Nuevo Cliente"
2. Complete los campos requeridos:
   - Nombre
   - Teléfono
   - Dirección
   - Email (opcional)
   - Límite de Crédito
3. Haga clic en "Guardar"

### Buscar Clientes
1. Use el campo de búsqueda en la parte superior
2. Ingrese nombre, teléfono o email
3. Haga clic en "Buscar"

### Editar o Eliminar Clientes
1. Seleccione un cliente de la lista
2. Use los botones "Editar" o "Eliminar"
3. Confirme la acción cuando se solicite

## Gestión de Productos

### Agregar un Nuevo Producto
1. En la pestaña "Productos", haga clic en "Nuevo Producto"
2. Complete los campos:
   - Nombre
   - Descripción
   - Precio
   - Stock Inicial
   - Stock Mínimo
   - Seleccione un Proveedor
3. Haga clic en "Guardar"

### Ajustar Stock
1. Seleccione un producto
2. Haga clic en "Ajustar Stock"
3. Ingrese la cantidad (positiva para aumentar, negativa para disminuir)
4. Ingrese el motivo del ajuste
5. Confirme la operación

### Alertas de Stock
- En la parte inferior de la pestaña se muestran los productos con stock bajo
- Se considera stock bajo cuando la cantidad es menor o igual al stock mínimo

## Gestión de Proveedores

### Agregar un Nuevo Proveedor
1. En la pestaña "Proveedores", haga clic en "Nuevo Proveedor"
2. Complete los campos:
   - Nombre
   - Teléfono
   - Email (opcional)
   - Dirección (opcional)
3. Haga clic en "Guardar"

### Gestionar Proveedores
- Use la búsqueda para filtrar proveedores
- Seleccione un proveedor para editar o eliminar

## Gestión de Ventas

### Registrar una Nueva Venta
1. En la pestaña "Ventas":
   - Seleccione un cliente
   - Seleccione un producto
   - Ingrese la cantidad
   - Haga clic en "Agregar"
2. Repita el proceso para agregar más productos
3. Verifique el total
4. Haga clic en "Finalizar Venta"

### Historial de Ventas
- Vea todas las ventas en la parte inferior
- Filtre por cliente o estado de pago
- Opciones disponibles:
  - Ver Detalles
  - Registrar Pago
  - Anular Venta

### Registrar Pagos
1. Seleccione una venta pendiente
2. Haga clic en "Registrar Pago"
3. Ingrese:
   - Monto
   - Método de Pago
   - Notas (opcional)
4. Confirme el pago

## Reportes

### Tipos de Reportes Disponibles
1. Ventas por Cliente
2. Productos más Vendidos
3. Balance de Pagos
4. Stock Actual

### Generar un Reporte
1. Seleccione el tipo de reporte
2. Ingrese rango de fechas (opcional)
3. Haga clic en "Generar"
4. Visualice el gráfico y los datos
5. Use "Exportar a Excel" para guardar el reporte

### Filtros de Reportes
- Fechas: Desde/Hasta
- Tipo de Reporte
- Los datos se actualizan automáticamente

## Consejos y Trucos

1. **Búsqueda Rápida**: Use la tecla Enter para buscar
2. **Alertas**: Revise regularmente las alertas de stock bajo
3. **Respaldos**: Exporte reportes regularmente para mantener registros
4. **Pagos**: Mantenga actualizados los pagos de clientes
5. **Stock**: Ajuste el stock mínimo según la demanda

## Solución de Problemas

### Problemas Comunes y Soluciones

1. **No se puede agregar venta**
   - Verifique que haya stock suficiente
   - Confirme que el cliente esté seleccionado

2. **Error en registro de pago**
   - Verifique que el monto no exceda el saldo pendiente
   - Confirme que la venta no esté anulada

3. **Producto no aparece**
   - Verifique que esté activo
   - Confirme que tenga stock disponible

4. **Reporte no se genera**
   - Verifique el formato de fechas (YYYY-MM-DD)
   - Confirme que haya datos en el período seleccionado 