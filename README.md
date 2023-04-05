# Сервис Async_API

## Общая информация
Сервис сделан в рамках обучения мидл python-разработчик на practicum.yandex.ru

API для получения информации о фильмах, персонах (актёры, режиссёры, сценаристы) и жанрах.

Реализовано на FastAPI. В качестве базы данных используется Elastic Search, в качестве кеша - Redis.

Подробности про методы и аргументы - см. `http://HOST:PORT/api/openapi`.

### Технологии

![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![ElasticSearch](https://img.shields.io/badge/-ElasticSearch-005571?style=for-the-badge&logo=elasticsearch)
## Запуск

Для запуска отдельно FastAPI-сервиса можно использовать докерфайл (например, если запускаем в k8s, предполагая, что у нас уже есть развёрнутый Elastic и прочая инфраструктура, и нужен только сам сервис). Используется порт 8000.

Для поднятия всего нужного окружения сразу (локально или для CI-тестов, например) можно использовать docker-compose (включает в себя сам сервис, Redis, Elastic и nginx). В этом случае используется порт 80 (nginx).

## ETL

ETL для первоначального заполнения Elastic'а данными из postgres находится в отдельном репозитории: https://github.com/AntonRev/Admin_panel.

## TEST

Для поднятия всего нужного окружения и запуска тестов можно использовать docker-compose (включает в себя сам сервис, тесты, Redis, Elastic, и nginx). 
Файл для запуска находится в `src/tests/functional/docer-compose.yaml`

