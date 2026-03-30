from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.async_database import get_async_db
from app.api.dependencies.auth import get_current_user
from app.models.models import User
from app.schemas.ai_coach import (
    ChatMessageRequest,
    ChatMessageResponse,
    ResumeReviewRequest,
    CoverLetterRequest,
    InterviewPrepRequest,
    SalaryNegotiationRequest,
    CareerPathRequest,
    ChatSessionResponse
)
from app.services.ai_coach_service import AiCoachService


router = APIRouter(prefix="/ai-coach", tags=["AI Coach"])


@router.post("/chat", response_model=ChatMessageResponse)
async def chat_with_coach(
    data: ChatMessageRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    return await AiCoachService.chat(db, current_user.id, data.message, data.session_id, data.context.value)


@router.post("/resume-review", response_model=Dict[str, Any])
async def review_resume(
    data: ResumeReviewRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    return await AiCoachService.review_resume(db, current_user.id, data.resume_text)


@router.post("/cover-letter", response_model=Dict[str, str])
async def generate_cover_letter(
    data: CoverLetterRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    return await AiCoachService.generate_cover_letter(db, current_user.id, data.job_description, data.tone.value)


@router.post("/interview-prep", response_model=Dict[str, Any])
async def prep_for_interview(
    data: InterviewPrepRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    return await AiCoachService.interview_prep(db, current_user.id, data.role, data.company)


@router.post("/salary-negotiation", response_model=Dict[str, Any])
async def negotiate_salary(
    data: SalaryNegotiationRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    return await AiCoachService.salary_negotiation(db, current_user.id, data)


@router.post("/career-path", response_model=Dict[str, Any])
async def map_career_path(
    data: CareerPathRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    return await AiCoachService.career_path(db, current_user.id, data.current_role, data.target_role)


@router.get("/sessions", response_model=List[ChatSessionResponse])
async def list_sessions(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    return await AiCoachService.get_chat_sessions(db, current_user.id)


@router.get("/sessions/{session_id}")
async def fetch_history(
    session_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    # Returns raw ORM models safely converting out through implicit serialization or custom mappings
    return await AiCoachService.get_chat_history(db, current_user.id, session_id)


@router.delete("/sessions/{session_id}", status_code=204)
async def remove_session(
    session_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    await AiCoachService.delete_chat_session(db, current_user.id, session_id)
