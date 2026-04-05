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


@router.get("/trending", response_model=List[JobResponse])
async def fetch_trending_jobs(
    limit: int = 10,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Fetches the highest velocity job arrays sorting organically by structural timestamps seamlessly.
    """
    return await JobService.get_trending_jobs(db, limit)

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

@router.get("/{job_id}/similar", response_model=List[JobResponse])
async def get_similar_jobs(
    job_id: int,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Computes heuristic Jaccard overlaps identifying strictly related Job arrays dynamically.
    """
    return await JobService.get_similar_jobs(db, job_id, limit)


@router.get("/{job_id}", response_model=JobResponse)
async def get_job_by_id(
    job_id: int,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Retrieve full details for a single job listing by ID.
    """
    return await JobService.get_job_by_id(db, job_id)
