import os
import webbrowser
from time import sleep

# Запускаем сервер в фоновом режиме
os.system("start cmd /k python manage.py runserver")

# Даем серверу время на запуск
sleep(3)

# Открываем браузер
webbrowser.open("http://127.0.0.1:8000/home/")