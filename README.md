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
