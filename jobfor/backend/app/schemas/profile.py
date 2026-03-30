from datetime import date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, HttpUrl

# ── Base Config ───────────────────────────────────────────────────

class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ── Profile ───────────────────────────────────────────────────────

class ProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    headline: Optional[str] = None
    summary: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None
    portfolio_url: Optional[HttpUrl] = None
    preferred_locations: Optional[List[str]] = None
    expected_salary_min: Optional[int] = None
    expected_salary_max: Optional[int] = None
    job_type_preference: Optional[List[str]] = None
    remote_preference: Optional[str] = None
    notice_period: Optional[str] = None
    career_interests: Optional[List[str]] = None


class ProfileResponse(ORMModel):
    id: int
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    headline: Optional[str] = None
    summary: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    preferred_locations: Optional[List[str]] = None
    experience_years: Optional[float] = None
    expected_salary_min: Optional[int] = None
    expected_salary_max: Optional[int] = None
    salary_currency: str
    job_type_preference: Optional[List[str]] = None
    remote_preference: Optional[str] = None
    notice_period: Optional[str] = None
    career_interests: Optional[List[str]] = None
    profile_completion: int


# ── Work Experience ───────────────────────────────────────────────

class WorkExperienceBase(BaseModel):
    company_name: str
    job_title: str
    employment_type: Optional[str] = None
    location: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    is_current: bool = False
    description: Optional[str] = None


class WorkExperienceCreate(WorkExperienceBase):
    pass


class WorkExperienceUpdate(BaseModel):
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    employment_type: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: Optional[bool] = None
    description: Optional[str] = None


class WorkExperienceResponse(WorkExperienceBase, ORMModel):
    id: int
    user_id: int
    skills_used: Optional[List[str]] = None


# ── Education ─────────────────────────────────────────────────────

class EducationBase(BaseModel):
    institution: str
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    grade: Optional[str] = None
    activities: Optional[str] = None


class EducationCreate(EducationBase):
    pass


class EducationUpdate(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    grade: Optional[str] = None
    activities: Optional[str] = None


class EducationResponse(EducationBase, ORMModel):
    id: int
    user_id: int


# ── Certification ─────────────────────────────────────────────────

class CertificationBase(BaseModel):
    name: str
    issuing_organization: str
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    credential_id: Optional[str] = None
    credential_url: Optional[HttpUrl] = None


class CertificationCreate(CertificationBase):
    pass


class CertificationUpdate(BaseModel):
    name: Optional[str] = None
    issuing_organization: Optional[str] = None
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    credential_id: Optional[str] = None
    credential_url: Optional[HttpUrl] = None


class CertificationResponse(CertificationBase, ORMModel):
    id: int
    user_id: int
    credential_url: Optional[str] = None

# ── Aggregated Profile Response ───────────────────────────────────
class FullProfileResponse(ProfileResponse):
    work_experiences: List[WorkExperienceResponse] = []
    educations: List[EducationResponse] = []
    certifications: List[CertificationResponse] = []
