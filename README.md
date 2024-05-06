# Tasks_TG_bot

[![CI/CD](https://github.com/alexpro2022/Tasks_TG_bot/actions/workflows/ci_cd.yml/badge.svg)](https://github.com/alexpro2022/Tasks_TG_bot/actions/workflows/ci_cd.yml)
[![codecov](https://codecov.io/gh/alexpro2022/Tasks_TG_bot/graph/badge.svg?token=ea3f5WxUb0)](https://codecov.io/gh/alexpro2022/Tasks_TG_bot)

<br>

## Оглавление
- [Технологии](#технологии)
- [Описание работы](#описание-работы)
- [Установка приложения](#установка-приложения)
- [Запуск тестов](#запуск-тестов)
- [Запуск приложения](#запуск-приложения)
- [Удаление приложения](#удаление-приложения)
- [Автор](#автор)

<br>

## Технологии
<details><summary>Подробнее</summary><br>

[![Python](https://img.shields.io/badge/python-3.12-blue?logo=python)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.5-blue?logo=aiogram)](https://aiogram.dev/)
[![Pydantic](https://img.shields.io/badge/pydantic-2.7-blue?logo=Pydantic)](https://docs.pydantic.dev/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)
[![asyncpg](https://img.shields.io/badge/-asyncpg-464646?logo=PostgreSQL)](https://pypi.org/project/asyncpg/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-blue?logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/-Alembic-464646?logo=alembic)](https://alembic.sqlalchemy.org/en/latest/)
[![docker_compose](https://img.shields.io/badge/-Docker%20Compose-464646?logo=docker)](https://docs.docker.com/compose/)
[![Pytest](https://img.shields.io/badge/-Pytest-464646?logo=Pytest)](https://docs.pytest.org/en/latest/)
[![Pytest-asyncio](https://img.shields.io/badge/-Pytest--asyncio-464646?logo=Pytest-asyncio)](https://pypi.org/project/pytest-asyncio/)
[![pytest-cov](https://img.shields.io/badge/-pytest--cov-464646?logo=codecov)](https://pytest-cov.readthedocs.io/en/latest/)
[![pre-commit](https://img.shields.io/badge/-pre--commit-464646?logo=pre-commit)](https://pre-commit.com/)

[⬆️Оглавление](#оглавление)

</details>

<br>

## Описание работы

Необходимо написать TG Бота, который будет создавать задачи через /add и добавлять их в БД PostgreSQL. Также по команде /tsk он должен выводить список задач из БД.

[⬆️Оглавление](#оглавление)

<br>

## Установка приложения:

<details><summary>Предварительные условия</summary>

Предполагается, что пользователь:
 - создал [бота](https://github.com/alexpro2022/instructions-t-bot/blob/main/README.md#%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5-%D0%B8-%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0-%D0%B0%D0%BA%D0%BA%D0%B0%D1%83%D0%BD%D1%82%D0%B0-%D0%B1%D0%BE%D1%82%D0%B0).
 - установил [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/) на локальной машине. Проверить наличие можно выполнив команды:

```bash
docker --version && docker-compose --version
```
<h1></h1></details>

<br>

Клонируйте репозиторий с GitHub и введите данные для переменных окружения (значения даны для примера, но их можно оставить):

```bash
git clone https://github.com/alexpro2022/Tasks_TG_bot.git
cd Tasks_TG_bot
cp env_example .env
nano .env
```

[⬆️Оглавление](#оглавление)

<br>

## Запуск тестов:
Из корневой директории проекта выполните команду запуска тестов:
```bash
docker compose -f docker/test/docker-compose.yml --env-file .env up --build --abort-on-container-exit && \
docker compose -f docker/test/docker-compose.yml --env-file .env down -v
```
После прохождения тестов в консоль будет выведен отчет pytest и coverage.

⬆️Оглавление

<br>

## Запуск приложения:

1. Из корневой директории проекта выполните команду:
```bash
docker compose -f docker/dev/docker-compose.yml --env-file .env up -d --build
```

2. Остановить docker и удалить контейнеры можно командой из корневой директории проекта:
```bash
docker compose -f docker/dev/docker-compose.yml --env-file .env down
```
Если также необходимо удалить том базы данных:
```bash
docker compose -f docker/dev/docker-compose.yml --env-file .env down -v && docker system prune -f
```

[⬆️Оглавление](#оглавление)

<br>

## Удаление приложения:
Из корневой директории проекта выполните команду:
```bash
cd .. && rm -fr Tasks_TG_bot
```

[⬆️Оглавление](#оглавление)

<br>

## Автор:
[Aleksei Proskuriakov](https://github.com/alexpro2022)

[⬆️В начало](#Tasks_TG_bot)
