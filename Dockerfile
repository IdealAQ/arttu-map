FROM python:3.11-slim

# Install uv from the official repository
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy mapping configuration files and source code
COPY pyproject.toml uv.lock ./
COPY ./src ./src

# Sync packages (this generates the /app/.venv pathing)
RUN uv sync --frozen --no-cache --no-install-project

EXPOSE 5006

# FIXED: Explicitly call the virtual environment python engine module directly
CMD [".venv/bin/python", "-m", "panel", "serve", "src/app.py", "--address", "0.0.0.0", "--port", "5006", "--allow-websocket-origin=*"]