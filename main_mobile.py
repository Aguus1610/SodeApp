from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.card import MDCard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

from modelo import *
from controlador import Controlador

class VentanaClientes(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controlador = Controlador()
        
        # Layout principal
        layout = BoxLayout(orientation='vertical')
        
        # Toolbar
        toolbar = MDTopAppBar(title="Clientes")
        layout.add_widget(toolbar)
        
        # Botón Agregar Cliente
        btn_agregar = MDRaisedButton(
            text="Nuevo Cliente",
            pos_hint={'center_x': .5},
            size_hint=(None, None)
        )
        layout.add_widget(btn_agregar)
        
        # Lista de clientes
        scroll = ScrollView()
        self.lista_clientes = MDList()
        scroll.add_widget(self.lista_clientes)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
        self.actualizar_lista()
    
    def actualizar_lista(self):
        self.lista_clientes.clear_widgets()
        clientes = self.controlador.obtener_todos_clientes()
        for cliente in clientes:
            item = OneLineListItem(
                text=f"{cliente.nombre} - {cliente.telefono}"
            )
            self.lista_clientes.add_widget(item)

class VentanaProductos(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        toolbar = MDTopAppBar(title="Productos")
        layout.add_widget(toolbar)
        self.add_widget(layout)

class VentanaVentas(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        toolbar = MDTopAppBar(title="Ventas")
        layout.add_widget(toolbar)
        self.add_widget(layout)

class VentanaReportes(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        toolbar = MDTopAppBar(title="Reportes")
        layout.add_widget(toolbar)
        self.add_widget(layout)

class GestionBebidasApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        # Navegación inferior
        navigation = MDBottomNavigation()
        
        # Pantallas
        screens = {
            'clientes': ('account', 'Clientes', VentanaClientes),
            'productos': ('package', 'Productos', VentanaProductos),
            'ventas': ('cart', 'Ventas', VentanaVentas),
            'reportes': ('chart', 'Reportes', VentanaReportes)
        }
        
        for id_screen, (icon, text, clase) in screens.items():
            screen = clase(name=id_screen)
            item = MDBottomNavigationItem(
                name=id_screen,
                text=text,
                icon=icon
            )
            item.add_widget(screen)
            navigation.add_widget(item)
            
        return navigation

if __name__ == '__main__':
    # Inicializar la base de datos
    inicializar_db()
    # Iniciar la aplicación
    GestionBebidasApp().run() 