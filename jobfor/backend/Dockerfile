# ─────────────────────────────────────────────
# Multi-stage Dockerfile — JobFor Backend
# Stage 1: builder   (installs deps)
# Stage 2: development (hot-reload)
# Stage 3: production  (final image)
# ─────────────────────────────────────────────

# ── Stage 1: Base Builder ──────────────────────────────────────
FROM python:3.12-slim AS builder

# Install system build deps for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies into an isolated prefix
# so we can copy just the installed packages to the next stage
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: Development ───────────────────────────────────────
FROM python:3.12-slim AS development

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Source is mounted as a volume in docker-compose (hot-reload)
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


# ── Stage 3: Production ────────────────────────────────────────
FROM python:3.12-slim AS production

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY . .

# Non-root user for security
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Gunicorn + uvicorn workers for production throughput
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", \
     "--workers", "4", "--proxy-headers", "--forwarded-allow-ips=*"]
