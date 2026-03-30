from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.async_database import get_async_db
from app.api.dependencies.auth import get_current_user
from app.models.models import User
from app.schemas.job import JobSearchParams, JobResponse, PaginatedJobResponse, RecommendedJobResponse
from app.services.job_service import JobService
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/search", response_model=PaginatedJobResponse)
async def search_jobs(
    params: JobSearchParams = Depends(),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Search and discover active jobs using dynamic filters.
    """
    return await JobService.search_jobs(db, params)

@router.get("/user/recommendations", response_model=List[RecommendedJobResponse])
async def get_job_recommendations(
    limit: int = 20,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    """
    Hybrid semantic job recommendations based on the logged-in user's profile metadata.
    Powered by scikit-learn TF-IDF and structured heuristic algorithms.
    """
    return await RecommendationService.get_recommendations(db, current_user.id, limit)

@router.get("/{job_id}", response_model=JobResponse)
async def get_job_by_id(
    job_id: int,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Retrieve full details for a single job listing by ID.
    """
    return await JobService.get_job_by_id(db, job_id)
