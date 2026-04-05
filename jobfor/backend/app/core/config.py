"""
app/core/config.py — Centralised application settings
======================================================
All values are read from environment variables (or a .env file).
Pydantic-settings handles type coercion and validation automatically.

Usage anywhere in the app::

    from app.core.config import settings
    print(settings.DATABASE_URL)
"""

from __future__ import annotations

from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",           # silently ignore unknown env vars
    )

    # ── Application ───────────────────────────────────────────
    PROJECT_NAME: str = "JobFor API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # ── Security ──────────────────────────────────────────────
    SECRET_KEY: str = "change-this-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24       # 24 h
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # ── PostgreSQL ────────────────────────────────────────────
    POSTGRES_USER: str = "jobfor"
    POSTGRES_PASSWORD: str = "jobfor_secret"
    POSTGRES_DB: str = "jobsearch"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    # If DATABASE_URL is set directly in .env (e.g. NeonDB), use it
    DATABASE_URL: str = ""

    @property
    def DB_URL(self) -> str:
        """Returns the effective database URL — prefers DATABASE_URL env var over parts."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    DB_ECHO: bool = False

    # ── Redis ─────────────────────────────────────────────────
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "redis_secret"
    REDIS_DB: int = 0
    # Upstash cloud Redis — used when local Redis is unavailable
    UPSTASH_REDIS_REST_URL: str = ""
    UPSTASH_REDIS_REST_TOKEN: str = ""

    @property
    def REDIS_URL(self) -> str:
        return (
            f"redis://:{self.REDIS_PASSWORD}"
            f"@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        )

    # ── CORS ──────────────────────────────────────────────────
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v):
        """Allow ALLOWED_ORIGINS to be a JSON string or a plain list."""
        if isinstance(v, str):
            import json
            return json.loads(v)
        return v

    # ── OpenAI / AI Coach ─────────────────────────────────────
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_MAX_TOKENS: int = 2048
    OPENAI_TEMPERATURE: float = 0.7
    AI_DAILY_TOKEN_BUDGET: int = 100_000      # per-user daily cap

    # ── Email ─────────────────────────────────────────────────
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAILS_FROM_EMAIL: str = "noreply@jobfor.ai"
    EMAILS_FROM_NAME: str = "JobFor"

    # ── File Storage (S3 / MinIO) ─────────────────────────────
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "jobfor-uploads"
    AWS_ENDPOINT_URL: str | None = None      # set for MinIO local dev

    # ── Celery ────────────────────────────────────────────────
    CELERY_BROKER_URL: str = "redis://:redis_secret@localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://:redis_secret@localhost:6379/2"

    # ── Job Market Integration API Keys ───────────────────────
    ADZUNA_APP_ID: str = ""
    ADZUNA_APP_KEY: str = ""
    RAPIDAPI_KEY: str = ""

    # ── Rate Limiting ─────────────────────────────────────────
    RATE_LIMIT_PER_MINUTE: int = 60

settings = Settings()
