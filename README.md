# Проектная работа 4 спринта

## Общая информация

API для получения информации о фильмах, персонах (актёры, режиссёры, сценаристы) и жанрах.

Реализовано на FastAPI. В качестве базы данных используется Elastic Search, в качестве кеша - Redis.

Подробности про методы и аргументы - см. http://HOST:PORT/api/openapi.

Репозиторий: https://github.com/AntonRev/Async_API_sprint_1/

## Запуск

Для запуска отдельно FastAPI-сервиса можно использовать докерфайл (например, если запускаем в k8s, предполагая, что у нас уже есть развёрнутый Elastic и прочая инфраструктура, и нужен только сам сервис). Используется порт 8000.

Для поднятия всего нужного окружения сразу (локально или для CI-тестов, например) можно использовать docker-compose (включает в себя сам сервис, Redis, Elastic и nginx). В этом случае используется порт 80 (nginx).

## ETL

ETL для первоначального заполнения Elastic'а данными из postgres находится в отдельном репозитории: https://github.com/AntonRev/new_admin_panel_sprint_3/.


## Исходное описание

**Важное сообщение для тимлида:** для ускорения проверки проекта укажите ссылку на приватный репозиторий с командной работой в файле readme и отправьте свежее приглашение на аккаунт [BlueDeep](https://github.com/BigDeepBlue).

В папке **tasks** ваша команда найдёт задачи, которые необходимо выполнить в первом спринте второго модуля.  Обратите внимание на задачи **00_create_repo** и **01_create_basis**. Они расцениваются как блокирующие для командной работы, поэтому их необходимо выполнить как можно раньше.

Мы оценили задачи в стори поинтах, значения которых брались из [последовательности Фибоначчи](https://ru.wikipedia.org/wiki/Числа_Фибоначчи) (1,2,3,5,8,…).

Вы можете разбить имеющиеся задачи на более маленькие, например, распределять между участниками команды не большие куски задания, а маленькие подзадачи. В таком случае не забудьте зафиксировать изменения в issues в репозитории.

**От каждого разработчика ожидается выполнение минимум 40% от общего числа стори поинтов в спринте.**
