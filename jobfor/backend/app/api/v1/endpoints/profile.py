from fastapi import APIRouter, Depends, status, File, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict

from app.core.async_database import get_async_db
from app.models.models import User
from app.api.dependencies.auth import get_current_user
from app.services.profile_service import ProfileService
from app.schemas.profile import (
    FullProfileResponse,
    ProfileUpdate,
    WorkExperienceCreate,
    WorkExperienceUpdate,
    WorkExperienceResponse,
    EducationCreate,
    EducationUpdate,
    EducationResponse,
    CertificationCreate,
    CertificationUpdate,
    CertificationResponse
)

router = APIRouter(prefix="/profile", tags=["profile"])

# ── Base Profile ──────────────────────────────────────────────────

@router.get("/", response_model=FullProfileResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """
    Fetch the complete profile of the currently authenticated user, 
    including experiences, educations, and certifications.
    """
    service = ProfileService(db)
    return await service.get_profile(current_user.id)


@router.put("/", response_model=FullProfileResponse)
async def update_my_profile(
    data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """
    Update strictly the base profile fields for the authenticated user.
    """
    service = ProfileService(db)
    return await service.update_profile(current_user.id, data)


# ── Work Experience ───────────────────────────────────────────────

@router.post("/experience", response_model=WorkExperienceResponse, status_code=status.HTTP_201_CREATED)
async def add_work_experience(
    data: WorkExperienceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """
    Add a new work experience entry to the user's profile.
    """
    service = ProfileService(db)
    return await service.add_work_experience(current_user.id, data)


@router.put("/experience/{exp_id}", response_model=WorkExperienceResponse)
async def update_work_experience(
    exp_id: int,
    data: WorkExperienceUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """
    Update an existing work experience entry.
    """
    service = ProfileService(db)
    return await service.update_work_experience(current_user.id, exp_id, data)


@router.delete("/experience/{exp_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work_experience(
    exp_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
) -> None:
    """
    Delete a work experience entry permanently.
    """
    service = ProfileService(db)
    await service.delete_work_experience(current_user.id, exp_id)


# ── Education ─────────────────────────────────────────────────────

@router.post("/education", response_model=EducationResponse, status_code=status.HTTP_201_CREATED)
async def add_education(
    data: EducationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """
    Add a new educational background entry.
    """
    service = ProfileService(db)
    return await service.add_education(current_user.id, data)


@router.put("/education/{edu_id}", response_model=EducationResponse)
async def update_education(
    edu_id: int,
    data: EducationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """
    Update an existing education entry.
    """
    service = ProfileService(db)
    return await service.update_education(current_user.id, edu_id, data)


@router.delete("/education/{edu_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_education(
    edu_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
) -> None:
    """
    Delete an education entry.
    """
    service = ProfileService(db)
    await service.delete_education(current_user.id, edu_id)


# ── Certifications ────────────────────────────────────────────────

@router.post("/certifications", response_model=CertificationResponse, status_code=status.HTTP_201_CREATED)
async def add_certification(
    data: CertificationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """
    Add a new certification or credential entry.
    """
    service = ProfileService(db)
    return await service.add_certification(current_user.id, data)


@router.put("/certifications/{cert_id}", response_model=CertificationResponse)
async def update_certification(
    cert_id: int,
    data: CertificationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """
    Update an existing certification.
    """
    service = ProfileService(db)
    return await service.update_certification(current_user.id, cert_id, data)


@router.delete("/certifications/{cert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_certification(
    cert_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
) -> None:
    """
    Delete a certification entry.
    """
    service = ProfileService(db)
    await service.delete_certification(current_user.id, cert_id)

# ── Resume Parsing ────────────────────────────────────────────────

from app.core.rate_limit import limiter
from fastapi import Request

@router.post("/resume", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
@limiter.limit("5/hour")
async def upload_resume(
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """
    Accepts explicit PDF document buffers, locally deploying via IO mapping,
    and processes NLP pipeline recursively updating the `UserSkill` junction cleanly.
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are structurally supported.")
        
    service = ProfileService(db)
    payload = await service.upload_and_parse_resume(current_user.id, file)
    
    return {
        "message": "Resume structured and processed successfully.",
        "data": payload
    }
