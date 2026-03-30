import pytest
from httpx import AsyncClient

# ── Dynamic Testing Vectors ──

global_user = {
    "email": "automated.test@jobfor.ai",
    "password": "SecureTest101!",
    "firstName": "Testing",
    "lastName": "Module"
}


@pytest.mark.asyncio
async def test_register_user_success(async_client: AsyncClient):
    """
    Validates native F-001 endpoints creating user arrays mapping successfully inside relational databases.
    Expects structured 201 headers alongside an active access/refresh payload.
    """
    response = await async_client.post(
        "/api/v1/auth/register",
        json=global_user
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "accessToken" in data
    assert "refreshToken" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_register_user_duplicate(async_client: AsyncClient):
    """
    Constructs an identical POST array validating the specific SQL 409 boundaries mapping directly back onto the front-end securely.
    """
    # 1. Initialize the global target
    await async_client.post("/api/v1/auth/register", json=global_user)
    
    # 2. Resend exact string explicitly testing constraint violations
    response = await async_client.post(
        "/api/v1/auth/register",
        json=global_user
    )
    
    assert response.status_code == 409
    data = response.json()
    assert "error" in data
    assert "already registered" in data["error"].lower()


@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient):
    """
    Executes standard login paths ensuring JWT strings safely dispatch alongside HTTP 200 checks natively.
    """
    # 1. Structure the database explicitly
    await async_client.post("/api/v1/auth/register", json=global_user)
    
    # 2. Request token via standard login payloads natively
    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": global_user["email"],
            "password": global_user["password"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "accessToken" in data
    assert "refreshToken" in data


@pytest.mark.asyncio
async def test_login_invalid_credentials(async_client: AsyncClient):
    """
    Maps corrupted passwords cleanly hitting FastAPI unauthed pipelines (401).
    """
    # 1. Register base user
    await async_client.post("/api/v1/auth/register", json=global_user)
    
    # 2. Corrupt structural inputs intentionally
    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": global_user["email"],
            "password": "IncorrectPassword123!"
        }
    )
    
    assert response.status_code == 401
    data = response.json()
    assert "error" in data
    assert "incorrect email or password" in data["error"].lower()
