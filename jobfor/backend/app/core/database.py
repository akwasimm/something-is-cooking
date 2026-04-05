"""
database.py — SQLAlchemy 2.0 Engine, Session & Base
====================================================
Provides:
  - Async-ready engine via psycopg2 (sync) or asyncpg (async)
  - `SessionLocal` scoped session factory
  - `Base` declarative base shared by all ORM models
  - `get_db()` FastAPI dependency for route-level DB injection
"""

from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────
# Engine
# ──────────────────────────────────────────────────────────────

engine = create_engine(
    settings.DB_URL,
    # Connection pool tuning — sensible defaults for a web service
    pool_size=10,            # max persistent connections
    max_overflow=20,         # extra connections allowed when pool is full
    pool_timeout=30,         # seconds to wait before raising OperationalError
    pool_recycle=1800,       # recycle connections every 30 min (avoids stale TCP)
    pool_pre_ping=True,      # test each connection with SELECT 1 before use
    echo=settings.DB_ECHO,   # set True in dev for SQL logging
)


# ──────────────────────────────────────────────────────────────
# SQLite compatibility shim (useful for local unit tests)
# ──────────────────────────────────────────────────────────────

@event.listens_for(engine, "connect")
def _set_sqlite_pragmas(dbapi_conn, connection_record):
    """Enable WAL mode and foreign keys when using SQLite (dev/testing)."""
    if "sqlite" in settings.DB_URL:
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


# ──────────────────────────────────────────────────────────────
# Session Factory
# ──────────────────────────────────────────────────────────────

SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=engine,
    autocommit=False,   # always explicit commits
    autoflush=False,    # flush manually for predictable behaviour
    expire_on_commit=False,  # keep model instances usable after commit
)


# ──────────────────────────────────────────────────────────────
# Declarative Base
# ──────────────────────────────────────────────────────────────

class Base(DeclarativeBase):
    """
    Shared declarative base for every ORM model.

    All models that inherit from this class are automatically registered
    with `Base.metadata`, which Alembic uses for migration autogeneration.
    """
    pass


# ──────────────────────────────────────────────────────────────
# FastAPI Dependency — per-request session
# ──────────────────────────────────────────────────────────────

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a transactional DB session.

    Usage in a route::

        @router.get("/items")
        def list_items(db: Session = Depends(get_db)):
            return db.query(Item).all()

    The session is automatically committed on success and rolled back
    on any unhandled exception, then closed either way.
    """
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ──────────────────────────────────────────────────────────────
# Context-manager helper (use outside of FastAPI, e.g. scripts)
# ──────────────────────────────────────────────────────────────

@contextmanager
def db_session() -> Generator[Session, None, None]:
    """
    Context-manager wrapper around `SessionLocal` for use in
    background tasks, CLI scripts, and Celery workers.

    Usage::

        with db_session() as db:
            db.add(some_model_instance)
    """
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ──────────────────────────────────────────────────────────────
# Startup utilities
# ──────────────────────────────────────────────────────────────

def init_db() -> None:
    """
    Create all tables defined in Base.metadata.

    Prefer Alembic migrations in production. This helper is useful
    for integration tests or first-time local setup.
    """
    # Import all models so they register with Base.metadata
    import app.models  # noqa: F401

    logger.info("Creating database tables…")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ready.")


def verify_connection() -> bool:
    """Perform a lightweight connectivity check against the database."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection verified ✓")
        return True
    except Exception as exc:  # noqa: BLE001
        logger.error("Database connection failed: %s", exc)
        return False
