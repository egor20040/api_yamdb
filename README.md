API_YAMDB

API_YAMDB - проект учебного API для сервиса отзывов к произведениям

АВТОРЫ:

Егор Мухаметвафин - https://github.com/emuhich

Роман Лосев - https://github.com/huli-net

Andrei Vedernikov - https://github.com/Andrei800


ЗАПУСК ПРОЕКТА


Клонировать репозиторий GitHub


Cоздать и активировать виртуальное окружение:

python -m venv env


Установить зависимости из файла requirements.txt:

python -m pip install --upgrade pip

pip install -r requirements.txt


Сделать миграции

python manage.py makemigrations

python manage.py migrate


Запустить проект

python3 manage.py runserver

Документация API YaMDb по адресу: http://127.0.0.1:8000/redoc/
