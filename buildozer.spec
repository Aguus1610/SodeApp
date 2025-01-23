[app]
title = SodeApp
package.name = sodeapp
package.domain = org.sodeapp

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db

version = 1.0
requirements = python3,kivy==2.1.0,kivymd==1.1.1,peewee==3.16.0,pillow==9.5.0,pandas==1.5.3,numpy==1.23.5

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.private_storage = True
android.accept_sdk_license = True
android.arch = arm64-v8a

# Lista de módulos Python que se incluirán
android.enable_androidx = True
android.bootstrap = sdl2

# Archivos para incluir
android.add_src = distribucion_bebidas.db:distribucion_bebidas.db

# Configuraciones adicionales
android.allow_backup = True
p4a.branch = master
p4a.bootstrap = sdl2
p4a.local_recipes = .

# Configuración de compilación
android.release_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1