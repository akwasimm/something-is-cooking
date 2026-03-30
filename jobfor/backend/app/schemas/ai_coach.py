from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict


class ChatContextEnum(str, Enum):
    general = "general"
    resume_review = "resume_review"
    interview_prep = "interview_prep"
    cover_letter = "cover_letter"
    salary_negotiation = "salary_negotiation"
    career_guidance = "career_guidance"


class ToneEnum(str, Enum):
    professional = "professional"
    enthusiastic = "enthusiastic"
    creative = "creative"


class ChatMessageRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    context: ChatContextEnum = ChatContextEnum.general


class ChatMessageResponse(BaseModel):
    session_id: str
    response: str
    tokens_used: Optional[int] = None


class ResumeReviewRequest(BaseModel):
    resume_text: str


class CoverLetterRequest(BaseModel):
    job_description: str
    tone: ToneEnum = ToneEnum.professional


class InterviewPrepRequest(BaseModel):
    role: str
    company: Optional[str] = None


class SalaryNegotiationRequest(BaseModel):
    current_offer: int
    role: str
    location: str
    years_of_experience: int


class CareerPathRequest(BaseModel):
    current_role: str
    target_role: str


class ChatSessionResponse(BaseModel):
    session_id: str
    message_count: int
    last_context: Optional[str] = None
