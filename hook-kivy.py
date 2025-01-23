from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Recopilar todos los submódulos de Kivy
hiddenimports = collect_submodules('kivy')

# Recopilar archivos de datos
datas = collect_data_files('kivy')

# Agregar dependencias específicas
hiddenimports.extend([
    'kivy.deps.sdl2',
    'kivy.deps.glew',
    'kivy.deps.angle',
    'kivy.factory_registers',
    'kivy.core.window',
    'kivy.core.text',
    'kivy.core.image',
    'kivy.core.audio'
]) 