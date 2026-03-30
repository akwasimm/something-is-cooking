from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class SkillDemand(BaseModel):
    skill: str
    demandPercentage: int


class LearningPathStep(BaseModel):
    week: int
    title: str
    resources: List[str]


class SkillGapResponse(BaseModel):
    targetRole: str
    readinessScore: float
    strongSkills: List[str]
    skillsToImprove: List[str]
    missingCritical: List[SkillDemand]
    learningPath: List[LearningPathStep]


class SalaryInsightResponse(BaseModel):
    role: str
    location: Optional[str] = None
    min: int
    median: int
    max: int
    sampleSize: int
