# Sistema de Gestión de Bebidas

## Descripción
Sistema completo para la gestión de distribuidoras de bebidas, que incluye manejo de inventario, clientes, proveedores, ventas y reportes.

## Requisitos del Sistema
- Windows 10 o superior
- 4GB de RAM mínimo
- 500MB de espacio en disco
- Python 3.8 o superior (para desarrollo)

## Instalación para Usuarios Finales
1. Descargue el archivo `GestionBebidas-Setup.exe`
2. Ejecute el instalador
3. Siga las instrucciones en pantalla
4. El programa creará un acceso directo en el escritorio

## Instalación para Desarrollo
1. Clone el repositorio:
```bash
git clone [url-del-repositorio]
```

2. Ejecute el script de instalación:
```bash
instalar.bat
```

3. El ejecutable se generará en la carpeta `build`

## Estructura del Proyecto
```
SodeApp/
├── main.py           # Punto de entrada de la aplicación
├── modelo.py         # Definición de la base de datos
├── vista.py          # Interfaz gráfica
├── controlador.py    # Lógica de negocio
├── utilidades.py     # Funciones auxiliares
├── graficos.py       # Generación de reportes gráficos
├── setup.py         # Configuración para generar ejecutable
├── instalar.bat     # Script de instalación
├── requirements.txt  # Dependencias del proyecto
├── manual_usuario.md # Manual de usuario
├── logs/            # Directorio para logs
└── graficos/        # Directorio para gráficos exportados
```

## Características Principales
- Gestión de clientes
- Control de inventario
- Registro de ventas
- Gestión de proveedores
- Reportes y estadísticas
- Exportación a Excel
- Sistema de alertas de stock

## Distribución
Para distribuir el software:
1. Ejecute `instalar.bat` para generar el ejecutable
2. Comprima la carpeta `build` generada
3. Distribuya el archivo comprimido a los usuarios finales

## Soporte
Para soporte técnico o consultas:
- Email: [su-email]
- Teléfono: [su-teléfono]

## Licencia
Todos los derechos reservados. Este software está protegido por leyes de propiedad intelectual. 