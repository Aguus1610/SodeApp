[app]
title = Gestión de Bebidas
package.name = gestionbebidas
package.domain = org.gestionbebidas

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db

version = 1.0
requirements = python3,kivy==2.2.1,kivymd==1.1.1,peewee==3.16.0,pillow==10.0.0,pandas==2.0.0,numpy==1.24.0

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1 