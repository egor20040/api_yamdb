Django-app workflow
Описание проекта:
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором.
В каждой категории есть произведения: книги, фильмы или музыка.
Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения (рейтинг). На одно произведение пользователь может оставить только один отзыв.
Полный список возможных запросов и соответствующих ответов можно найти в документации "Redoc".

Как зарегистрироваться и получить JWT-токен
Отправьте POST-запрос с параметрами email и username на эндпоинт /api/v1/auth/signup/;
Сервис YaMDB отправит вас письмо с кодом подтверждения (confirmation_code) на указанный адрес email;
Отправьте POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/. В ответе на запрос вы получите JWT-token;
После регистрации и получения токена можете отправить PATCH-запрос на эндпоинт /api/v1/users/me/ и заполнить поля в своём профайле (описание полей — в документации).
Теперь вы можете работать с API проекта, отправляя полученный токен при каждом запросе :)
Документация API YaMDb по адресу: http://127.0.0.1:8000/redoc/

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
