"""
app/core/redis.py — Redis client factory
=========================================
Provides a singleton synchronous Redis client for use in:
  - Route-level rate limiting
  - Session / token caching
  - Job alert queue signalling
  - Market insight cache reads/writes

For async contexts (WebSocket, background tasks), use `aioredis` instead.
"""

from __future__ import annotations

import logging
from functools import lru_cache

import redis

from app.core.config import settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_redis_client() -> redis.Redis:
    """
    Return a singleton synchronous Redis client.

    The client is connection-pool-backed by default so it is safe to
    share across threads in a multi-worker uvicorn deployment.

    Usage::

        from app.core.redis import get_redis_client
        r = get_redis_client()
        r.set("key", "value", ex=300)
    """
    client = redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,        # always return str, not bytes
        max_connections=20,
        socket_connect_timeout=5,
        socket_timeout=5,
        retry_on_timeout=True,
    )
    logger.debug("Redis client initialised → %s", settings.REDIS_URL)
    return client


def ping_redis() -> bool:
    """Return True if Redis responds to PING, False otherwise."""
    try:
        return get_redis_client().ping()
    except redis.RedisError as exc:
        logger.warning("Redis ping failed: %s", exc)
        return False
