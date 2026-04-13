"""
migrations/env.py — Alembic runtime environment
================================================
Responsibilities:
  - Override sqlalchemy.url from app.core.config (reads .env)
  - Import ALL models so Base.metadata is fully populated
  - Support both offline (SQL script generation) and online modes
  - Configure autogenerate comparison options for JSONB, Enums, etc.
"""

from __future__ import annotations

import logging
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool, text

from alembic import context

# ── Make `app` importable when running `alembic` from ./backend ──
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings  # noqa: E402
from app.core.database import Base   # noqa: E402

# ── Import ALL models so they register with Base.metadata ────────
import app.models  # noqa: F401, E402  — side-effect import is intentional

logger = logging.getLogger("alembic.env")

# ── Alembic Config object ─────────────────────────────────────────
config = context.config

# Override the URL from settings (respects .env at runtime)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Set up Python logging from alembic.ini [loggers] section
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# The metadata object Alembic reads for autogenerate
target_metadata = Base.metadata


# ─────────────────────────────────────────────────────────────────
# Helper: autogenerate comparison configuration
# ─────────────────────────────────────────────────────────────────

def include_object(obj, name, type_, reflected, compare_to):
    """
    Filter out tables/objects we do NOT want Alembic to manage.

    Views created in migration 002 are excluded so that autogenerate
    doesn't try to drop them when it compares against `reflected`.
    """
    _excluded_views = {"user_complete_profile", "user_application_stats"}
    if type_ == "table" and name in _excluded_views:
        return False
    return True


# ─────────────────────────────────────────────────────────────────
# Offline mode — generates a .sql script without a live DB connection
# ─────────────────────────────────────────────────────────────────

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    Useful for generating SQL scripts to review before applying,
    or when the database is not yet reachable (CI/CD pipelines).
    """
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,          # detect column type changes
        compare_server_default=True,
        include_object=include_object,
        # Render PostgreSQL-specific types correctly in generated SQL
        render_as_batch=False,
    )

    with context.begin_transaction():
        context.run_migrations()

    logger.info("Offline migration SQL generated.")


# ─────────────────────────────────────────────────────────────────
# Online mode — applies migrations directly to a live database
# ─────────────────────────────────────────────────────────────────

def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode against a live PostgreSQL instance.

    Uses NullPool so that the migration process doesn't hold an idle
    connection open after `alembic upgrade head` completes.
    """
    section = config.get_section(config.config_ini_section, {})
    section["sqlalchemy.url"] = config.get_main_option("sqlalchemy.url")
    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    print("!!! MIGRATING AGAINST URL !!! :", repr(connectable.url))
    with connectable.connect() as connection:
        # Verify connectivity before attempting migrations
        connection.execute(text("SELECT 1"))
        logger.info("Database connection verified — running migrations.")

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,           # detect column type changes
            compare_server_default=True, # detect server_default changes
            include_object=include_object,
            # Render enums correctly in autogenerate diffs
            include_schemas=False,
            transaction_per_migration=True,  # each migration in its own txn
        )

        with context.begin_transaction():
            context.run_migrations()

    logger.info("Migrations complete.")


# ─────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
