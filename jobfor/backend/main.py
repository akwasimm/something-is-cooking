"""
main.py — FastAPI application entry point
==========================================
Configures:
  - Lifespan: DB ping + Redis ping on startup/shutdown
  - CORS middleware
  - Global exception handler
  - OpenAPI metadata
  - API v1 router
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

import redis as sync_redis
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import verify_connection

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────
# Lifespan — startup & shutdown events
# ─────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Execute startup checks before serving requests and teardown on exit.

    Startup:
      1. Verify PostgreSQL connectivity.
      2. Verify Redis connectivity.
    Shutdown:
      - Log graceful shutdown.
    """
    # ── Startup ───────────────────────────────────────────────
    logger.info("🚀 JobFor API starting up…")

    # PostgreSQL check
    if not verify_connection():
        logger.critical("❌ PostgreSQL is unreachable — aborting startup.")
        raise RuntimeError("Cannot connect to PostgreSQL.")
    logger.info("✅ PostgreSQL connected.")

    # Redis check
    try:
        r = sync_redis.from_url(settings.REDIS_URL, decode_responses=True)
        r.ping()
        r.close()
        logger.info("✅ Redis connected.")
    except Exception as exc:
        logger.critical("❌ Redis is unreachable: %s — aborting startup.", exc)
        raise RuntimeError("Cannot connect to Redis.") from exc

    # Scheduler Init
    from app.services.scheduler_service import start_scheduler
    logger.info("🕒 Initializing Background Sync Scheduler...")
    start_scheduler()

    logger.info("✅ All services healthy. Serving requests.")

    yield  # ← application runs here

    # ── Shutdown ──────────────────────────────────────────────
    logger.info("👋 JobFor API shutting down gracefully.")


# ─────────────────────────────────────────────────────────────────
# Application factory
# ─────────────────────────────────────────────────────────────────

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "AI-powered Job Search Assistant API.\n\n"
        "Provides job search, AI career coaching, application tracking, "
        "and market insights for candidates."
    ),
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
    contact={
        "name": "JobFor Engineering",
        "url": "https://github.com/your-org/jobfor",
    },
    license_info={"name": "MIT"},
)


# ─────────────────────────────────────────────────────────────────
# Middleware
# ─────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────────────────────────
# Global exception handlers
# ─────────────────────────────────────────────────────────────────

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Return consistent JSON error envelopes for HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code,
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Catch-all for unexpected server errors — never leak tracebacks."""
    logger.exception("Unhandled exception on %s %s", request.method, request.url)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "An unexpected error occurred. Please try again.",
            "status_code": 500,
        },
    )


# ─────────────────────────────────────────────────────────────────
# Routers
# ─────────────────────────────────────────────────────────────────

app.include_router(api_router, prefix=settings.API_V1_STR)


# ─────────────────────────────────────────────────────────────────
# Root endpoints
# ─────────────────────────────────────────────────────────────────

@app.get("/", tags=["Root"], summary="Root health check")
def root():
    """Lightweight liveness probe — returns immediately without DB I/O."""
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running",
        "docs": f"{settings.API_V1_STR}/docs",
    }


@app.get("/health", tags=["Root"], summary="Deep health check")
def health_check():
    """
    Deep health check — verifies database connectivity.
    Used by Docker / Kubernetes readiness probes.
    """
    db_ok = verify_connection()
    status_code = 200 if db_ok else 503

    try:
        r = sync_redis.from_url(settings.REDIS_URL, decode_responses=True)
        redis_ok = r.ping()
        r.close()
    except Exception:
        redis_ok = False

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "healthy" if (db_ok and redis_ok) else "degraded",
            "services": {
                "postgresql": "up" if db_ok else "down",
                "redis": "up" if redis_ok else "down",
            },
        },
    )
