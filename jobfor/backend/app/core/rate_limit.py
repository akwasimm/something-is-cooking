from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings

# Use in-memory storage if Redis is unavailable (dev-friendly fallback)
# In production, ensure Redis is running and REDIS_URL is correctly set
import redis as _redis
import logging
_logger = logging.getLogger(__name__)

_storage_uri: str
try:
    _r = _redis.from_url(settings.REDIS_URL, socket_connect_timeout=2)
    _r.ping()
    _r.close()
    _storage_uri = settings.REDIS_URL
    _logger.info("Rate limiter using Redis backend: %s", settings.REDIS_HOST)
except Exception:
    _storage_uri = "memory://"
    _logger.warning("⚠️  Redis unavailable — rate limiter using in-memory storage (not suitable for production)")

limiter = Limiter(key_func=get_remote_address, storage_uri=_storage_uri)
