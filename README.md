# Questions & Answers API

A RESTful API for a Q&A system built with FastAPI and PostgreSQL.
Allows managing questions and answers through HTTP requests (GET, POST, DELETE).
Swagger documentation is available after application startup.

## Technologies

- FastAPI - web framework
- PostgreSQL - database
- SQLAlchemy 2.0 - ORM
- Alembic - migrations
- Docker - containerization
- Pydantic - data validation

## Requirements

- Docker and Docker Compose
- Working PostgreSQL
- Configured .env file

## Installation

Clone the repository:
```bash
git clone https://github.com/irolltwenties/testquest.git
```

# Setup

## Update .env file

Create or update the `.env` file with the following variables:
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
## Update Alembic configuration

Update the `alembic.ini` file with the following database URL format:
```ini
sqlalchemy.url = postgresql+psycopg2://${TEST_QUEST_DB_LOGIN}:${TEST_QUEST_DB_PASSWORD}@${TEST_QUEST_DB_HOST}:${TEST_QUEST_DB_PORT}/${TEST_QUEST_DB_NAME}
```
**Note:** While the application uses asyncpg, Alembic prefers synchronous drivers, hence psycopg2 is used (included in requirements.txt).

# Running with Docker Compose

Start all services in detached mode:
```bash
docker compose up -d
```
View application logs:
```bash
docker compose logs -f <container name or id default testquest-api-1>
```
# API Documentation

After application startup, documentation is available at:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Ensure port 8000 is exposed from the Docker container to access the documentation.

# Running Tests

Run tests with coverage:
```bash
docker compose exec api pytest --cov
```
# Testing with Postman

Import the collection from: `TEST_QUEST_API.postman_collection.json`

# Troubleshooting

## Database Connection Errors

Ensure that:
- PostgreSQL container is running (`docker-compose ps`)
- .env file variables are correct
- Network ports are not occupied

## Migration Errors

Try restarting migrations:
```bash
docker compose exec api alembic downgrade base
docker compose exec api alembic upgrade head
```

# Bench research
[See the research](./BENCH.md)

