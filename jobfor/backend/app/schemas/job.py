from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


class JobSearchParams(BaseModel):
    query: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[List[str]] = None
    experience_level: Optional[List[str]] = None
    salary_min: Optional[int] = None
    remote: Optional[bool] = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1)


class JobResponse(BaseModel):
    id: int
    external_id: Optional[str] = None
    title: str
    company: str
    location: Optional[str] = None
    description: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    currency: str
    is_remote: bool
    skills_required: Optional[List[str]] = None
    apply_url: Optional[str] = None
    posted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PaginatedJobResponse(BaseModel):
    data: List[JobResponse]
    total: int
    page: int
    limit: int


class MatchBreakdown(BaseModel):
    skills: float
    content: float
    experience: float
    location: float
    salary: float


class RecommendedJobResponse(JobResponse):
    match_score: float
    match_breakdown: MatchBreakdown

    model_config = ConfigDict(from_attributes=True)
