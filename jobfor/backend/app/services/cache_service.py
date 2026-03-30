"""
app/services/cache_service.py — Async Redis Cache Service
==========================================================
Provides a high-level, type-safe interface over `redis.asyncio`
for use across the FastAPI application.

Features:
  • Async connection pool shared across the app lifecycle
  • JSON serialisation / deserialisation for arbitrary Python objects
  • TTL-based expiry on all set operations
  • Pattern-based bulk invalidation
  • Decorator `@cached()` for route-level caching

Usage::

    from app.services.cache_service import CacheService

    cache = CacheService()

    # In a route:
    data = await cache.get_cache("jobs:trending")
    if data is None:
        data = expensive_db_query()
        await cache.set_cache("jobs:trending", data, expire_in_seconds=300)

    # Delete a key:
    await cache.delete_cache("jobs:trending")

    # Decorator usage:
    @cached(key="skills:all", ttl=600)
    async def get_all_skills(db): ...
"""

from __future__ import annotations

import functools
import json
import logging
from typing import Any, Callable, TypeVar

import redis.asyncio as aioredis
from redis.asyncio.connection import ConnectionPool

from app.core.config import settings

log = logging.getLogger(__name__)

# ── Type alias for the decorator ───────────────────────────────
F = TypeVar("F", bound=Callable[..., Any])


# ══════════════════════════════════════════════════════════════════════════════
# Connection Pool — module-level singleton
# ══════════════════════════════════════════════════════════════════════════════

_pool: ConnectionPool | None = None


def _get_pool() -> ConnectionPool:
    """
    Return a module-level connection pool, creating it on first call.

    The pool is shared across all `CacheService` instances so we never
    open more connections than `max_connections` regardless of how many
    concurrent requests are being handled.
    """
    global _pool
    if _pool is None:
        _pool = aioredis.ConnectionPool.from_url(
            settings.REDIS_URL,
            max_connections=20,
            decode_responses=True,      # always return str / dict, not bytes
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True,
        )
        log.debug("Redis async connection pool created → %s", settings.REDIS_URL)
    return _pool


async def close_redis_pool() -> None:
    """
    Gracefully close the shared Redis connection pool.

    Call this from the FastAPI `lifespan` shutdown event.
    """
    global _pool
    if _pool is not None:
        await _pool.aclose()
        _pool = None
        log.info("Redis connection pool closed.")


# ══════════════════════════════════════════════════════════════════════════════
# Cache Service
# ══════════════════════════════════════════════════════════════════════════════

class CacheService:
    """
    Async Redis cache service with JSON serialisation.

    All public methods silently handle `RedisError` exceptions and log
    them — a cache failure should never crash the application.

    Parameters
    ----------
    key_prefix : Optional namespace prepended to every key,
                 e.g. ``CacheService(key_prefix="users:")``
    """

    DEFAULT_TTL: int = 300          # 5 minutes
    MAX_TTL: int = 86_400           # 24 hours

    def __init__(self, key_prefix: str = "") -> None:
        self._prefix = key_prefix

    # ── Internal helpers ─────────────────────────────────────────

    def _client(self) -> aioredis.Redis:
        """Return a Redis client bound to the shared pool."""
        return aioredis.Redis(connection_pool=_get_pool())

    def _key(self, key: str) -> str:
        """Apply the optional namespace prefix."""
        return f"{self._prefix}{key}"

    @staticmethod
    def _serialise(value: Any) -> str:
        """Serialise any Python object to a JSON string."""
        return json.dumps(value, default=str, ensure_ascii=False)

    @staticmethod
    def _deserialise(raw: str | None) -> Any:
        """Deserialise a JSON string back to a Python object."""
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            # Return the raw string if it's not valid JSON
            return raw

    # ── Core CRUD Methods ────────────────────────────────────────

    async def get_cache(self, key: str) -> Any:
        """
        Retrieve a cached value by key.

        Parameters
        ----------
        key : Cache key (prefix is applied automatically).

        Returns
        -------
        Any
            The deserialised cached value, or ``None`` if the key does
            not exist or has expired.
        """
        full_key = self._key(key)
        try:
            async with self._client() as r:
                raw = await r.get(full_key)
            if raw is None:
                log.debug("Cache MISS → %s", full_key)
                return None
            log.debug("Cache HIT  → %s", full_key)
            return self._deserialise(raw)
        except aioredis.RedisError as exc:
            log.warning("Redis GET failed for key '%s': %s", full_key, exc)
            return None

    async def set_cache(
        self,
        key: str,
        value: Any,
        expire_in_seconds: int = DEFAULT_TTL,
    ) -> bool:
        """
        Store a value in the cache with an expiry TTL.

        Parameters
        ----------
        key              : Cache key.
        value            : Any JSON-serialisable Python object.
        expire_in_seconds: Time-to-live in seconds (default: 5 min).
                           Clamped to MAX_TTL (24h).

        Returns
        -------
        bool
            ``True`` if the value was stored successfully, ``False`` otherwise.
        """
        full_key = self._key(key)
        ttl = min(max(1, expire_in_seconds), self.MAX_TTL)
        try:
            serialised = self._serialise(value)
            async with self._client() as r:
                await r.setex(full_key, ttl, serialised)
            log.debug("Cache SET  → %s (TTL %ds, %d bytes)", full_key, ttl, len(serialised))
            return True
        except aioredis.RedisError as exc:
            log.warning("Redis SET failed for key '%s': %s", full_key, exc)
            return False

    async def delete_cache(self, key: str) -> bool:
        """
        Delete a single cached key.

        Parameters
        ----------
        key : Cache key to delete.

        Returns
        -------
        bool
            ``True`` if the key was deleted, ``False`` if it did not exist
            or an error occurred.
        """
        full_key = self._key(key)
        try:
            async with self._client() as r:
                deleted = await r.delete(full_key)
            hit = bool(deleted)
            log.debug("Cache DEL  → %s (%s)", full_key, "found" if hit else "not found")
            return hit
        except aioredis.RedisError as exc:
            log.warning("Redis DEL failed for key '%s': %s", full_key, exc)
            return False

    # ── Extra Utility Methods ────────────────────────────────────

    async def exists(self, key: str) -> bool:
        """Return True if the key exists in the cache."""
        full_key = self._key(key)
        try:
            async with self._client() as r:
                return bool(await r.exists(full_key))
        except aioredis.RedisError as exc:
            log.warning("Redis EXISTS failed for key '%s': %s", full_key, exc)
            return False

    async def ttl(self, key: str) -> int:
        """
        Return remaining TTL in seconds for a key.

        Returns -2 if key does not exist, -1 if key has no expiry.
        """
        full_key = self._key(key)
        try:
            async with self._client() as r:
                return await r.ttl(full_key)
        except aioredis.RedisError as exc:
            log.warning("Redis TTL failed for key '%s': %s", full_key, exc)
            return -2

    async def invalidate_pattern(self, pattern: str) -> int:
        """
        Delete all keys matching a glob pattern.

        Example: ``await cache.invalidate_pattern("jobs:*")``

        .. warning::
            Uses SCAN (cursor-based) not KEYS — safe for production.

        Returns
        -------
        int
            Number of keys deleted.
        """
        full_pattern = self._key(pattern)
        deleted = 0
        try:
            async with self._client() as r:
                async for key in r.scan_iter(match=full_pattern, count=100):
                    await r.delete(key)
                    deleted += 1
            log.debug("Cache PURGE → pattern '%s' removed %d keys.", full_pattern, deleted)
        except aioredis.RedisError as exc:
            log.warning("Redis SCAN/DEL failed for pattern '%s': %s", full_pattern, exc)
        return deleted

    async def get_or_set(
        self,
        key: str,
        factory: Callable[[], Any],
        expire_in_seconds: int = DEFAULT_TTL,
    ) -> Any:
        """
        Return cached value if it exists, otherwise call `factory()`,
        cache the result, and return it.

        Parameters
        ----------
        key              : Cache key.
        factory          : Zero-argument async or sync callable that
                           returns the value to cache on a miss.
        expire_in_seconds: TTL for the newly cached value.

        Example::

            data = await cache.get_or_set(
                key="skills:all",
                factory=lambda: db.execute(select(Skill)).scalars().all(),
                expire_in_seconds=600,
            )
        """
        cached = await self.get_cache(key)
        if cached is not None:
            return cached

        import asyncio
        if asyncio.iscoroutinefunction(factory):
            value = await factory()
        else:
            value = factory()

        await self.set_cache(key, value, expire_in_seconds)
        return value

    async def ping(self) -> bool:
        """Return True if Redis is reachable."""
        try:
            async with self._client() as r:
                return await r.ping()
        except aioredis.RedisError:
            return False


# ══════════════════════════════════════════════════════════════════════════════
# Route-level Caching Decorator
# ══════════════════════════════════════════════════════════════════════════════

def cached(
    key: str,
    ttl: int = CacheService.DEFAULT_TTL,
    key_prefix: str = "",
) -> Callable[[F], F]:
    """
    Decorator that caches the return value of an async function.

    The decorated function's result is stored under `key` with the given TTL.
    On cache hit the function body is skipped entirely.

    Parameters
    ----------
    key        : Static cache key.
    ttl        : Time-to-live in seconds.
    key_prefix : Optional namespace prefix.

    Example::

        @cached(key="skills:all", ttl=600)
        async def get_all_skills(db: AsyncSession) -> list[dict]:
            result = await db.execute(select(Skill))
            return [s.name for s in result.scalars()]
    """
    _cache = CacheService(key_prefix=key_prefix)

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            cached_value = await _cache.get_cache(key)
            if cached_value is not None:
                return cached_value
            result = await func(*args, **kwargs)
            await _cache.set_cache(key, result, expire_in_seconds=ttl)
            return result
        return wrapper  # type: ignore[return-value]
    return decorator


# ══════════════════════════════════════════════════════════════════════════════
# Pre-built named instances (import these in your routes)
# ══════════════════════════════════════════════════════════════════════════════

# Generic cache — no prefix
cache = CacheService()

# Namespaced instances for cleaner key management
job_cache        = CacheService(key_prefix="jobs:")
user_cache       = CacheService(key_prefix="users:")
skill_cache      = CacheService(key_prefix="skills:")
insight_cache    = CacheService(key_prefix="insights:")
rate_limit_cache = CacheService(key_prefix="ratelimit:")
