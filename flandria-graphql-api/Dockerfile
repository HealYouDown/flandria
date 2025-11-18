FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

CMD ["/app/.venv/bin/uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "4"]