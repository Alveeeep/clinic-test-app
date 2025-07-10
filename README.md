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
