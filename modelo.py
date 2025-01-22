from datetime import datetime
from peewee import *
from typing import List, Optional

# Configuración de la base de datos
db = SqliteDatabase('distribucion_bebidas.db')

class BaseModel(Model):
    class Meta:
        database = db

class Proveedor(BaseModel):
    nombre = CharField(max_length=100)
    telefono = CharField(max_length=20)
    email = CharField(max_length=100, null=True)
    direccion = TextField(null=True)
    activo = BooleanField(default=True)
    fecha_registro = DateTimeField(default=datetime.now)

class Producto(BaseModel):
    nombre = CharField(max_length=100)
    descripcion = TextField(null=True)
    precio_unitario = DecimalField(decimal_places=2, auto_round=True)
    stock_actual = IntegerField(default=0)
    stock_minimo = IntegerField(default=10)
    proveedor = ForeignKeyField(Proveedor, backref='productos')
    activo = BooleanField(default=True)
    fecha_actualizacion = DateTimeField(default=datetime.now)

class Cliente(BaseModel):
    nombre = CharField(max_length=100)
    telefono = CharField(max_length=20)
    email = CharField(max_length=100, null=True)
    direccion = TextField()
    fecha_registro = DateTimeField(default=datetime.now)
    activo = BooleanField(default=True)
    limite_credito = DecimalField(decimal_places=2, default=0)

class Venta(BaseModel):
    cliente = ForeignKeyField(Cliente, backref='ventas')
    fecha = DateTimeField(default=datetime.now)
    total = DecimalField(decimal_places=2, default=0)
    pagada = BooleanField(default=False)
    notas = TextField(null=True)

class DetalleVenta(BaseModel):
    venta = ForeignKeyField(Venta, backref='detalles')
    producto = ForeignKeyField(Producto, backref='ventas')
    cantidad = IntegerField()
    precio_unitario = DecimalField(decimal_places=2)
    subtotal = DecimalField(decimal_places=2)

class Pago(BaseModel):
    venta = ForeignKeyField(Venta, backref='pagos')
    fecha = DateTimeField(default=datetime.now)
    monto = DecimalField(decimal_places=2)
    metodo_pago = CharField(max_length=50)
    notas = TextField(null=True)

def inicializar_db():
    """Inicializa la base de datos creando todas las tablas necesarias."""
    db.connect()
    db.create_tables([
        Proveedor,
        Producto,
        Cliente,
        Venta,
        DetalleVenta,
        Pago
    ])
    db.close()

if __name__ == '__main__':
    inicializar_db() 