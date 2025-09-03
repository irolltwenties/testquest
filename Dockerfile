FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE ${TEST_QUEST_API_PORT:-8000}

CMD ["sh", "-c", "alembic upgrade head && python main.py --host ${TEST_QUEST_API_HOST:-0.0.0.0} --port ${TEST_QUEST_API_PORT:-8000}"]