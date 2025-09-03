# Questions & Answers API

RESTful API для системы вопросов и ответов на FastAPI + PostgreSQL.
Позволяет работать с вопросами и ответами на них с помощью http-запросов (GET, POST, DELETE).
После запуска приложения будет доступна swagger-документация.

## Технологии

- FastAPI - веб-фреймворк
- PostgreSQL - база данных  
- SQLAlchemy 2.0 - ORM
- Alembic - миграции
- Docker - контейнеризация
- Pydantic - валидация данных

## Требования для работы

- Docker и Docker Compose
- рабочий PostgreSQL
- Настроенный .env файл

# Запуск
Клонируем репозиторий:
```bash
git clone https://github.com/irolltwenties/testquest.git
```

## Подготовка к старту
### Обновление .env файла
```bash
# Database
TEST_QUEST_DB_LOGIN=your_db_user
TEST_QUEST_DB_PASSWORD=your_strong_password
TEST_QUEST_DB_NAME=testques_db
TEST_QUEST_DB_HOST=localhost
TEST_QUEST_DB_PORT=5432

# API
TEST_QUEST_API_HOST=0.0.0.0
TEST_QUEST_API_PORT=8000
```
### Обновление конфигурационных файлов alembic
Для корректного запуска миграций следует обновить файл alembic.ini, по образцу ниже.
```bash
sqlalchemy.url = postgresql+psycopg2://${TEST_QUEST_DB_LOGIN}:${TEST_QUEST_DB_PASSWORD}@${TEST_QUEST_DB_HOST}:${TEST_QUEST_DB_PORT}/${TEST_QUEST_DB_NAME}
```
Хотя само приложение использует asyncpg, alembic предпочитает синхронные драйвера, поэтому в ссылке именно psycopg2 (так же есть в requirements.txt)
## Запуск через docker-compose

```bash
# Запуск всех сервисов
docker compose up -d

# Просмотр логов
docker compose logs -f api
```

# Документация API
После запуска приложения доступны:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

Для доступа к документации из Docker контейнера убедитесь, что порт 8000 проброшен на хост
# Запуск тестов
```bash
docker compose exec api pytest --cov
```
## Тестирование через Postman
Импортируйте коллекцию из postman/QnA_API.postman_collection.json

## Troubleshooting
### Ошибка подключения к БД
Убедитесь что:
- PostgreSQL контейнер запущен (docker-compose ps)
- Переменные в .env файле правильные
- Сетевые порты не заняты
### Ошибка в ходе миграций
Можно попробовать перезапустить миграции
```bash
docker compose exec api alembic downgrade base
docker compose exec api alembic upgrade head
```