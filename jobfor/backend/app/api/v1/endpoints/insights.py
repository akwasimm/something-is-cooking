from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.async_database import get_async_db
from app.api.dependencies.auth import get_current_user
from app.models.models import User
from app.schemas.insights import SalaryInsightResponse, SkillDemand, SkillGapResponse, CompanyInsightResponse
from app.services.insights_service import InsightsService


router = APIRouter(prefix="/insights", tags=["Analytics & Insights"])


@router.get("/salary", response_model=SalaryInsightResponse)
async def fetch_salary_trend(
    role: str,
    location: Optional[str] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """
    Real-time dynamically cached salary aggregation calculations scoping jobs specifically by title and location.
    """
    return await InsightsService.get_salary_insights(db, role, location)


@router.get("/skills/demand", response_model=List[SkillDemand])
async def fetch_job_market_demand(
    limit: int = 20,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """
    Extract natively indexed tags weighting specific skills as a percentile mapped against the active database.
    """
    return await InsightsService.get_skill_demand(db, limit)


@router.get("/skill-gap", response_model=SkillGapResponse)
async def analyze_career_gap(
    role: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """
    Matches the user's specific skill structure dynamically against the top indexed market demands for a role, explicitly generating an AI-curated curriculum road-map bridging the numeric percentage void.
    """
    return await InsightsService.analyze_skill_gap(db, current_user.id, role)


@router.get("/companies", response_model=List[CompanyInsightResponse])
async def fetch_mass_hiring_companies(
    limit: int = 20,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """
    Aggregates native database rows sorting companies dynamically tracking Mass Hiring volumes entirely.
    """
    return await InsightsService.get_company_insights(db, limit)
