# Тестовое задание «Clinic Appointments»

## Использованные технологии:

### - [PostgreSQL](https://www.postgresql.org)

### - [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)

### - [Alembic](https://github.com/sqlalchemy/alembic)

### - [FastApi](https://github.com/fastapi/fastapi)

### Линтеры: black, isort, flake8

### Пакетный менеджер [uv](https://github.com/astral-sh/uv)

## Запуск линтеров и тестов:

### Через Makefile:

```sh
make check
```

## Запуск тестовой среды и тестов через [docker compose](https://docs.docker.com/compose/):

```sh
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

## Запуск продакшн версии:

### Через Makefile:

```sh
make up
```

### Через docker compose:

```sh
docker compose up -d --build
```

# Док-артефакты

## [Ссылка на miro](https://miro.com/app/board/uXjVJfNW2Ek=/?share_link_id=576076514083)

## Архитектура:

![architecture.jpg](docs%2Farchitecture.jpg)

## Структура БД:

### Таблица Appointments:

- id - идентификатор записи
- patient_name - имя пациента
- doctor_id - идентификатор врача
- start_time - время начала
- created_at - дата создания записи
- updated_at - дата обновления записи

### Также реализован [Unique Constraint](https://docs.sqlalchemy.org/en/20/core/constraints.html#:~:text=support%20with%20SQLite-,UNIQUE%20Constraint,-%C2%B6) из SQLAlchemy, чтобы не записать к одному врачу двух пациентов на одно время

## Activity-диаграмма

![activity.jpg](docs%2Factivity.jpg)

## Документ бизнес-процесса

![proccess.jpg](docs%2Fproccess.jpg)

## Проектирование и реализация

![realization.jpg](docs%2Frealization.jpg)

# Телеграм-бот с ИИ-подбором врача

1. Бот узнает у пациента, какой врач нужен, какая дата посещения была бы удобна.
2. Отправляет запрос к модели, с заранее прописанным промптом (например: ты менеджер в клинике и должен выдать есть ли возможность клиенту записаться, либо вернуть ближайшее свободное время для этого врача)
3. В идеале, клиент может предоставлять куда больше информации, которая также пойдет в обработку модели
4. Если клиента устраивает предложенное время или его время для записи подходит, то отправляется post запрос к api для создания записи
5. Для работы с ИИ можно обращаться по API напрямую, например openai.api, или использовать LangChain для построения AI агента