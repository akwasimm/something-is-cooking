import pytest
from httpx import AsyncClient

# ── Dependency Mocking ──

mock_user = {
    "email": "job_searcher@jobfor.ai",
    "password": "SecurePassword101!",
    "firstName": "Job",
    "lastName": "Hunter"
}

async def _get_auth_headers(async_client: AsyncClient) -> dict:
    """Helper explicitly building user contexts registering tokens securely."""
    await async_client.post("/api/v1/auth/register", json=mock_user)
    response = await async_client.post("/api/v1/auth/login", json={
        "email": mock_user["email"],
        "password": mock_user["password"]
    })
    token = response.json()["accessToken"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_search_jobs_success(async_client: AsyncClient):
    """
    Validates basic search capabilities asserting raw structure returns correctly parsing generic arrays.
    """
    response = await async_client.get("/api/v1/jobs/search?query=software")
    
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total" in data
    assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_search_jobs_filters(async_client: AsyncClient):
    """
    Triggers explicit boolean logic (`remote=true`) forcing structured constraint validations dynamically mapping limits.
    """
    response = await async_client.get(
        "/api/v1/jobs/search",
        params={
            "query": "react",
            "remote": "true",
            "salary_min": 100000,
            "limit": 5
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["limit"] == 5


@pytest.mark.asyncio
async def test_get_recommendations_success(async_client: AsyncClient):
    """
    Assesses AI-Recommendation matrix ensuring ML floats parse natively explicitly requiring an active `Bearer` token natively mapping against `User` models.
    """
    headers = await _get_auth_headers(async_client)
    
    response = await async_client.get(
        "/api/v1/jobs/user/recommendations",
        headers=headers
    )
    
    # Asserting 200 assumes the DB and Model returned the sequence cleanly
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    
    # Evaluates specifically the added ML fields correctly merged
    if data["data"]:
        # Verifies the ML pipeline injected match metrics completely natively
        assert "match_score" in data["data"][0]
        assert "match_breakdown" in data["data"][0]


@pytest.mark.asyncio
async def test_get_recommendations_unauthorized(async_client: AsyncClient):
    """
    Explicitly forces Protected 401 routes blocking recommendation calls devoid of Token Authentication natively natively guarding AI loads securely.
    """
    response = await async_client.get("/api/v1/jobs/user/recommendations")
    
    assert response.status_code == 401
    data = response.json()
    assert "error" in data
    assert "not authenticated" in data["error"].lower()
