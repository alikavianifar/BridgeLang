# ── Stage 1: Base ────────────────────────────
FROM python:3.12-slim AS base

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Install system dependencies required for PostgreSQL and Pillow
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        libjpeg62-turbo-dev \
        zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# ── Stage 2: Dependencies ───────────────────
FROM base AS dependencies

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Stage 3: Application ────────────────────
FROM dependencies AS application

# Copy project files
COPY . .

# Collect static files (uses default/env SECRET_KEY)
RUN python manage.py collectstatic --noinput 2>/dev/null || true

# Expose the application port
EXPOSE 8000

# Run with gunicorn in production
CMD ["gunicorn", "CoreFolder.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
