# api_yamdb

![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

## Описание проекта:

* Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором.
* В каждой категории есть произведения: книги, фильмы или музыка. 
* Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.
* Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения (рейтинг). На одно произведение пользователь может оставить только один отзыв.

Полный список возможных запросов и соответствующих ответов можно найти в документации "Redoc".
 
## Как зарегистрироваться и получить *JWT-токен*

1. Отправьте POST-запрос с параметрами *email* и *username* на эндпоинт ```/api/v1/auth/signup/```;
2. Сервис YaMDB отправит вас письмо с кодом подтверждения (*confirmation_code*) на указанный адрес *email*;
3. Отправьте POST-запрос с параметрами *username* и *confirmation_code* на эндпоинт ```/api/v1/auth/token/```. В ответе на запрос вы получите *JWT-token*;
4. После регистрации и получения токена можете отправить PATCH-запрос на эндпоинт ```/api/v1/users/me/``` и заполнить поля в своём профайле (описание полей — в документации).

### Теперь вы можете работать с API проекта, отправляя полученный токен при каждом запросе :) ###

## Настройка и запуск проекта:


Клонировать репозиторий [GitHub](https://github.com/emuhich/api_yamdb)

Cоздать и активировать виртуальное окружение:
```python
python -m venv env
```
Установить зависимости из файла requirements.txt:

```python
python -m pip install --upgrade pip

pip install -r requirements.txt
```

Сделать миграции

```python
python manage.py makemigrations

python manage.py migrate
```

Запустить проект

```python
python3 manage.py runserver
```

### Авторы:

[Егор Мухаметвафин](https://github.com/emuhich)

[Роман Лосев](https://github.com/huli-net)

[Andrei Vedernikov](https://github.com/Andrei800)
