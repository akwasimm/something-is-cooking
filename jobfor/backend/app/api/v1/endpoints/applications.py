from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.async_database import get_async_db
from app.api.dependencies.auth import get_current_user
from app.models.models import User, ApplicationStatus
from app.schemas.application import (
    SaveJobCreate, 
    SavedJobResponse, 
    JobApplicationCreate, 
    JobApplicationResponse, 
    ApplicationStatusUpdate
)
from app.services.application_service import ApplicationService


router = APIRouter(prefix="/applications", tags=["ats"])


@router.post("/saved", response_model=SavedJobResponse)
async def save_job(
    data: SaveJobCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    return await ApplicationService.save_job(db, current_user.id, data)


@router.get("/saved", response_model=List[SavedJobResponse])
async def get_saved_jobs(
    folder: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    return await ApplicationService.get_saved_jobs(db, current_user.id, folder)


@router.delete("/saved/{job_id}", status_code=204)
async def unsave_job(
    job_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    await ApplicationService.unsave_job(db, current_user.id, job_id)
    

@router.post("/apply", response_model=JobApplicationResponse)
async def apply_to_job(
    data: JobApplicationCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    return await ApplicationService.apply_to_job(db, current_user.id, data)


@router.get("/", response_model=List[JobApplicationResponse])
async def get_applications(
    status: Optional[ApplicationStatus] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    return await ApplicationService.get_applications(db, current_user.id, status)


@router.patch("/{app_id}/status", response_model=JobApplicationResponse)
async def update_application_status(
    app_id: int,
    data: ApplicationStatusUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    return await ApplicationService.update_application_status(db, current_user.id, app_id, data)


@router.get("/stats", response_model=Dict[str, Any])
async def get_application_stats(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    return await ApplicationService.get_application_stats(db, current_user.id)
