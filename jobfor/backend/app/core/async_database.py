"""
app/core/async_database.py — SQLAlchemy 2.0 Async Engine & Session
===================================================================
Provides the async counterpart to `database.py` (which is synchronous
and used by Alembic + FastAPI sync routes).

This module is used exclusively by:
  - Background ingestion scripts (ingest_jobs.py)
  - Celery async tasks
  - Any async FastAPI route that opts in

Driver: asyncpg (postgresql+asyncpg://)
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import text

from app.core.config import settings

logger = logging.getLogger(__name__)


# ── Async Engine ────────────────────────────────────────────────

def _build_async_url() -> str:
    """Convert psycopg2/postgres URL to an asyncpg-compatible async URL."""
    base = settings.DATABASE_URL  # e.g. postgresql://... or postgresql+psycopg2://...
    if base:
        # Strip any existing driver suffix, then reattach asyncpg
        url = base.split("://", 1)
        if len(url) == 2:
            return f"postgresql+asyncpg://{url[1]}"
    # Fallback: build from individual parts
    return (
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    )


async_engine = create_async_engine(
    _build_async_url(),
    pool_size=10,
    max_overflow=20,
    pool_recycle=1800,
    pool_pre_ping=True,
    echo=settings.DB_ECHO,
)

# ── Async Session Factory ───────────────────────────────────────

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=async_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# ── FastAPI Dependency ──────────────────────────────────────────

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields an async DB session.

    Usage::

        @router.get("/items")
        async def list_items(db: AsyncSession = Depends(get_async_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# ── Context Manager (scripts / tasks) ──────────────────────────

@asynccontextmanager
async def async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async context manager for use outside FastAPI (scripts, workers).

    Usage::

        async with async_db_session() as db:
            db.add(instance)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# ── Connectivity Check ──────────────────────────────────────────

async def verify_async_connection() -> bool:
    """Async lightweight DB ping."""
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Async database connection verified ✓")
        return True
    except Exception as exc:
        logger.error("Async database connection failed: %s", exc)
        return False
