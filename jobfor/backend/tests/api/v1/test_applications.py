import pytest
from httpx import AsyncClient

# ── Dependency Mocking ──

mock_user = {
    "email": "ats_tester@jobfor.ai",
    "password": "SecurePassword101!",
    "firstName": "Testing",
    "lastName": "Applicant"
}

mock_job_id = "external-api-job-id-001"
mock_job_data = {
    "title": "Senior Vue Developer",
    "company": "FakeCorp Inc",
    "location": "Mumbai, MH"
}

async def _get_auth_headers(async_client: AsyncClient) -> dict:
    """Helper explicitly building user contexts generating token authorization payload natively."""
    await async_client.post("/api/v1/auth/register", json=mock_user)
    response = await async_client.post("/api/v1/auth/login", json={
        "email": mock_user["email"],
        "password": mock_user["password"]
    })
    token = response.json()["accessToken"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_save_job_success(async_client: AsyncClient):
    """
    Evaluates tracking mechanics explicitly caching new boolean flags tying native users onto saved JSONB targets correctly.
    """
    headers = await _get_auth_headers(async_client)
    
    response = await async_client.post(
        "/api/v1/applications/saved",
        json={
            "job_id": mock_job_id,
            "job_data": mock_job_data,
            "folder": "Wishlist"
        },
        headers=headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["job_id"] == mock_job_id
    assert data["folder"] == "Wishlist"


@pytest.mark.asyncio
async def test_save_job_duplicate(async_client: AsyncClient):
    """
    Explicitly prevents tracking the same application multiple times raising hard 400 constraints efficiently saving DB bloat.
    """
    headers = await _get_auth_headers(async_client)
    payload = {"job_id": mock_job_id, "job_data": mock_job_data}
    
    # 1. Trigger initial save loop
    await async_client.post("/api/v1/applications/saved", json=payload, headers=headers)
    
    # 2. Re-trigger the duplicated constraint implicitly testing exception borders
    response = await async_client.post("/api/v1/applications/saved", json=payload, headers=headers)
    
    assert response.status_code == 400
    assert "already saved" in response.json()["error"].lower()


@pytest.mark.asyncio
async def test_apply_job_success(async_client: AsyncClient):
    """
    Generates new Application pipelines marking users cleanly inside "applied" Funnel tracking enumerators seamlessly!
    """
    headers = await _get_auth_headers(async_client)
    
    response = await async_client.post(
        "/api/v1/applications/apply",
        json={
            "job_id": "different-job-id-002",
            "job_data": {"title": "Fullstack Java"},
            "resume_used": "Main Resume",
            "notes": "Emailed recruiter matching criteria natively."
        },
        headers=headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "applied"
    assert data["job_id"] == "different-job-id-002"
    assert "resume_used" in data


@pytest.mark.asyncio
async def test_apply_job_duplicate(async_client: AsyncClient):
    """
    Explicitly guards applied status metrics rejecting secondary applications spanning duplicate job listings naturally!
    """
    headers = await _get_auth_headers(async_client)
    payload = {
        "job_id": "different-job-id-002",
        "job_data": {"title": "Fullstack Java"}
    }
    
    # Apply iteration 1
    await async_client.post("/api/v1/applications/apply", json=payload, headers=headers)
    
    # Apply iteration 2 triggering 400 boundaries cleanly
    response = await async_client.post("/api/v1/applications/apply", json=payload, headers=headers)
    
    assert response.status_code == 400
    assert "already submitted" in response.json()["error"].lower()
