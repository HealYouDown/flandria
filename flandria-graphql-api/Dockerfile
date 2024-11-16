# Poetry builder stage
FROM python:3.12-slim AS builder

ARG POETRY_VERSION=1.8.3

ENV POETRY_HOME=/opt/poetry \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Tell Poetry where to place its cache and virtual environment
    POETRY_CACHE_DIR=/opt/.cache

RUN pip install "poetry==${POETRY_VERSION}"

# Needed to build psycopg2 later
RUN apt-get update && apt-get -y install libpq-dev gcc

WORKDIR /app
COPY pyproject.toml .
RUN poetry install --no-root --without dev && rm -rf $POETRY_CACHE_DIR

# Runtime stage
FROM python:3.12-slim AS runtime
WORKDIR /app
EXPOSE 5000

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    NUMBER_OF_WORKERS=4

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY . .

CMD uvicorn src.api.app:app --host 0.0.0.0 --port 5000 --workers $NUMBER_OF_WORKERS