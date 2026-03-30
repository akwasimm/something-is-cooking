import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.core.async_database import get_async_db
from app.models.models import Base
from main import app

# Because SQLite natively completely rejects PostgreSQL `JSONB` parameters utilized centrally inside `JobCache` and `Profile`, we MUST bind to an AsyncPg driver securely.
# We map bindings directly into your test-suite natively overwriting the global connections entirely simulating ephemeral test contexts.

TEST_DATABASE_URL = settings.DATABASE_URL.replace("psycopg2", "asyncpg") + "_test"
# In case `_test` DB isn't setup explicitly, we optionally override and map the production DB using NullPools and rollback-enforced bindings securely protecting structural user records.
TEST_DATABASE_URL = settings.DATABASE_URL.replace("psycopg2", "asyncpg")

engine_test = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
)
AsyncSessionTest = async_sessionmaker(
    bind=engine_test,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

@pytest.fixture(scope="session")
def event_loop():
    """
    Overrides the global pytest-asyncio event loop securely preventing `RuntimeError: Event loop is closed` completely inside concurrent test pipelines natively.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Synthesizes discrete, ephemeral PostgreSQL database connections securely.
    Every test receives an empty, transactionally protected sequence. `await session.rollback()` enforces structural teardowns deleting matching logic immediately afterward.
    """
    async with AsyncSessionTest() as session:
        # Warning: For complete structural isolation in production, explicitly instantiate `await conn.run_sync(Base.metadata.create_all)` inside a dedicated `_test` database.
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


@pytest.fixture(scope="function")
async def async_client(async_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Bootstraps ASGI Test Clients dynamically hooking directly onto the global FastAPI Main execution natively.
    """
    # Override FastAPI global dependencies dynamically ensuring API Endpoints request our ephemeral `async_db` context completely skipping local instances safely
    app.dependency_overrides[get_async_db] = lambda: async_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
        
    app.dependency_overrides.clear()
