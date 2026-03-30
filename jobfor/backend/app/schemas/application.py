from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict, Field

from app.models.models import ApplicationStatus


class SaveJobCreate(BaseModel):
    job_id: str
    job_data: Dict[str, Any]
    notes: Optional[str] = None
    folder: str = Field(default="default")
    tags: Optional[List[str]] = None


class SavedJobResponse(BaseModel):
    id: int
    user_id: int
    job_id: Optional[int] = None
    external_job_id: Optional[str] = None
    job_data: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    tags: Optional[List[Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class JobApplicationCreate(BaseModel):
    job_id: str
    job_data: Dict[str, Any]
    resume_used: Optional[str] = None
    cover_letter: Optional[str] = None
    notes: Optional[str] = None


class JobApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_id: Optional[int] = None
    external_job_id: Optional[str] = None
    job_data: Optional[Dict[str, Any]] = None
    status: ApplicationStatus
    applied_at: datetime
    status_updated_at: Optional[datetime] = None
    resume_used: Optional[str] = None
    cover_letter: Optional[str] = None
    notes: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    interview_dates: Optional[List[Any]] = None
    feedback: Optional[str] = None
    salary_offered: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus
    notes: Optional[str] = None
    interview_date: Optional[datetime] = None
    follow_up_date: Optional[datetime] = None
