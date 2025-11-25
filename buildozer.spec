[app]

# Имя приложения
title = WordUp

# Пакет (обязательно латиница)
package.name = wordup
package.domain = org.example

# Версия
version = 1.0

# Главный файл
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,db

# Иконка (можно не трогать)
# icon.filename = assets/koala.png

# Ориентация
orientation = portrait

# Разрешения
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE

# Требования
requirements = python3,kivy==2.3.1,kivymd==1.2.0,sqlite3

# Включаем базу данных
presplash.filename = assets/koala.png