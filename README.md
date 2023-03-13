# Продуктовый помощник Foodgram

## Описание

Проект "Foodgram" является онлайн-сервисом с API. При помощи этого сервиса пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Проект размещен на Яндекс.Облаке c IP 158.160.20.235.
(IP динамический, может измениться)

## Установка

* Для установки на сервер потребуется установить Docker и Docker Compose:
    ```
    sudo apt install docker-ce docker-compose -y
    ```
* Склонируйте проект на сервер:
    ```
    git clone git@github.com:P1oot/foodgram-project-react.git
    ```
* В репозитории infra необходимо создать файл .env:
    ```
    cd infra/
    touch .env
    nano .env
    ```
* Его необходимо заполнить следующими строками:
    ```
    DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
    DB_NAME=postgres # имя базы данных
    POSTGRES_USER=postgres # логин для подключения к базе данных
    POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
    DB_HOST=db # название сервиса (контейнера)
    DB_PORT=5432 # порт для подключения к БД 
    ```
* Запустить docker-compose (-d для работы в фоновом режиме):
    ```
    docker-compose up -d
    ```
* Выполнить миграции, создать суперпользователя и собрать статику:
    ```
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    docker-compose exec web python manage.py collectstatic --no-input
    ```
* Теперь проект доступен по Вашему IP

## Примеры запросов

Обращение к пользователям: "http://158.160.20.235/api/users/{id}/"

Обращение к рецептам: "http://158.160.20.235/api/recipes/{id}/"

Обращение к ингредиетам: "http://158.160.20.235/api/ingredients/{id}"

Обращение к тегам: "http://158.160.20.235/api/tags/{id}"

Более подробно с описанием запросов можно ознакомиться по адресу: "http://158.160.20.235/api/docs/redoc.html"

## Для проверки проекта

email: dan.berdinskikh@yandex.ru

password: dan1234
