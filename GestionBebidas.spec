# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('vista.py', '.'), ('modelo.py', '.'), ('controlador.py', '.'), ('graficos.py', '.'), ('utilidades.py', '.')],
    hiddenimports=['kivy', 'kivy.core.window.window_sdl2', 'kivy.core.text.text_sdl2', 'kivy.core.text.markup', 'kivy.core.image', 'kivy.core.audio.audio_sdl2', 'kivy.uix.behaviors', 'kivy.uix.recycleview', 'kivy.factory_registers', 'kivy.graphics', 'kivy.graphics.texture', 'kivy.graphics.vertex', 'kivy.graphics.compiler', 'kivy.loader', 'kivy.support', 'kivy.core.clipboard', 'kivy.core.clipboard.clipboard_sdl2', 'kivymd', 'kivymd.uix.behaviors', 'kivymd.uix.dialog', 'kivymd.uix.button', 'kivymd.uix.list', 'kivymd.icon_definitions', 'PIL', 'PIL._imagingtk', 'PIL._tkinter_finder', 'peewee', 'pandas', 'numpy', 'tkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tensorflow', 'torch', 'scipy', 'sphinx', 'keras', 'pyarrow', 'pygments', 'IPython', 'jupyter', 'docutils', 'colorama'],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GestionBebidas',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GestionBebidas',
)
