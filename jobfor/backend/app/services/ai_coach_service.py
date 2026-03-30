import uuid
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

from fastapi import HTTPException
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from openai import AsyncOpenAI

from app.core.config import settings
from app.models.models import ChatHistory, Profile, User, MessageType
from app.schemas.ai_coach import (
    ChatMessageResponse,
    SalaryNegotiationRequest,
    ChatSessionResponse
)

# Async singleton explicitly loading from .env setup
openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


class AiCoachService:

    @staticmethod
    async def chat(db: AsyncSession, user_id: int, message: str, session_id: Optional[str] = None, context_tag: str = "general") -> ChatMessageResponse:
        # Resolve distinct conversational namespace ID
        session_uuid = uuid.UUID(session_id) if session_id else uuid.uuid4()

        # 1. Fetch deep profile state
        stmt_prof = (
            select(Profile)
            .where(Profile.user_id == user_id)
            .options(
                selectinload(Profile.user).selectinload(User.skills),
                selectinload(Profile.user).selectinload(User.work_experiences)
            )
        )
        cursor = await db.execute(stmt_prof)
        profile = cursor.scalars().first()
        
        # Hydrate text-heavy context
        if profile:
            skill_text = ", ".join([s.skill.name for s in profile.user.skills]) if profile.user.skills else "None explicitly listed."
            exp_text = " ".join([f"{e.job_title} at {e.company_name}." for e in profile.user.work_experiences])
            context_string = f"User Profile Background: Headline: {profile.headline}. Summary: {profile.summary}. Skills: {skill_text}. Experience: {exp_text}."
        else:
            context_string = "User profile is incomplete."

        # 2. Extract preceding conversation loop
        hist_stmt = (
            select(ChatHistory)
            .where(ChatHistory.session_id == session_uuid)
            .order_by(ChatHistory.created_at.asc())
        )
        hist_cursor = await db.execute(hist_stmt)
        prior_messages = hist_cursor.scalars().all()

        messages = [
            {"role": "system", "content": f"You are an expert AI Career Coach named Jobfor AI. Answer concisely. Use this context: {context_string}"}
        ]
        
        for p_msg in prior_messages:
            role = "assistant" if p_msg.message_type == MessageType.assistant else "user"
            messages.append({"role": role, "content": p_msg.content})
            
        messages.append({"role": "user", "content": message})

        # 3. Transmit matrix memory securely to OpenAI
        try:
            response = await openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7
            )
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"AI Provider error: {str(e)}")

        ai_reply = response.choices[0].message.content
        tokens = response.usage.total_tokens

        # 4. Synchronously archive Request & Response objects in local DB limits
        user_hist = ChatHistory(
            user_id=user_id,
            session_id=session_uuid,
            message_type=MessageType.user,
            content=message,
            metadata_={"context": context_tag}
        )
        ai_hist = ChatHistory(
            user_id=user_id,
            session_id=session_uuid,
            message_type=MessageType.assistant,
            content=ai_reply,
            tokens_used=tokens,
            metadata_={"context": context_tag}
        )
        db.add_all([user_hist, ai_hist])
        await db.commit()

        return ChatMessageResponse(
            session_id=str(session_uuid),
            response=ai_reply,
            tokens_used=tokens
        )

    @staticmethod
    async def review_resume(db: AsyncSession, user_id: int, resume_text: str) -> Dict[str, Any]:
        prompt = f"""You are an ATS optimization specialist viewing raw resume text. 
        Analyze it strictly returning a JSON matrix containing these exact keys:
        'overallScore' (int 1-100), 'strengths' (list of strings), 'improvements' (list of strings), 'suggestions' (list of strings), 'atsScore' (int 1-100).
        
        Resume:
        {resume_text}
        """
        
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="AI returned malformed JSON payload.")

    @staticmethod
    async def generate_cover_letter(db: AsyncSession, user_id: int, job_description: str, tone: str) -> Dict[str, str]:
        prompt = f"""Write a modern, compelling cover letter in a {tone} tone targeting this job description:
        {job_description}
        
        Return a strict JSON object containing two keys:
        'primary_letter' (a comprehensive full-length letter),
        'alternative_variation' (a shorter, highly direct email version).
        """
        
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(response.choices[0].message.content)

    @staticmethod
    async def interview_prep(db: AsyncSession, user_id: int, role: str, company: Optional[str]) -> Dict[str, Any]:
        company_ctx = f" specifically at {company}" if company else ""
        prompt = f"""Generate an expert interview preparation guide for a {role} position{company_ctx}.
        Return a JSON object with:
        'common_questions' (list of strings),
        'star_scenarios' (list of dicts spanning 'scenario', 'action', 'result'),
        'tips' (list of strings).
        """
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(response.choices[0].message.content)

    @staticmethod
    async def salary_negotiation(db: AsyncSession, user_id: int, data: SalaryNegotiationRequest) -> Dict[str, Any]:
        prompt = f"""Provide tactical salary negotiation advice.
        Current Offer: {data.current_offer}. Role: {data.role}. Location: {data.location}. Experience: {data.years_of_experience} years.
        
        Return JSON object with keys:
        'market_benchmark' (string estimate),
        'counter_offer_strategies' (list of strings),
        'email_template' (string).
        """
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(response.choices[0].message.content)

    @staticmethod
    async def career_path(db: AsyncSession, user_id: int, current_role: str, target_role: str) -> Dict[str, Any]:
        prompt = f"""Create a career transition roadmap bridging from '{current_role}' to '{target_role}'.
        Return a JSON object featuring:
        'milestones' (list of dicts: 'step_name', 'timeline', 'action_items' list),
        'recommended_skills' (list of strings),
        'resources' (list of strings).
        """
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}]
        )
        return json.loads(response.choices[0].message.content)

    @staticmethod
    async def get_chat_sessions(db: AsyncSession, user_id: int) -> List[ChatSessionResponse]:
        # Using a specialized GroupBy equivalent strictly over ChatHistory structure
        stmt = (
            select(
                ChatHistory.session_id,
                # Explicit group mappings might fail cleanly in SqlAlchemy 2 without text, using raw count cleanly per session
            )
            .where(ChatHistory.user_id == user_id)
            .group_by(ChatHistory.session_id)
        )
        # Because we want complex grouping, we'll fetch all scalar and unique them in memory for clean dict assembly
        # In extremely large tables this could slow down, but for chat history it's manageable.
        pass_stmt = select(ChatHistory).where(ChatHistory.user_id == user_id).order_by(desc(ChatHistory.created_at))
        cursor = await db.execute(pass_stmt)
        histories = cursor.scalars().all()
        
        session_map = {}
        for h in histories:
            s_id = str(h.session_id)
            if s_id not in session_map:
                context = h.metadata_.get("context", "general") if h.metadata_ else "general"
                session_map[s_id] = {"session_id": s_id, "message_count": 0, "last_context": context}
            session_map[s_id]["message_count"] += 1

        return [ChatSessionResponse(**v) for v in session_map.values()]

    @staticmethod
    async def get_chat_history(db: AsyncSession, user_id: int, session_id: str) -> List[ChatHistory]:
        stmt = (
            select(ChatHistory)
            .where(
                ChatHistory.user_id == user_id,
                ChatHistory.session_id == uuid.UUID(session_id)
            ).order_by(ChatHistory.created_at.asc())
        )
        cursor = await db.execute(stmt)
        return list(cursor.scalars().all())

    @staticmethod
    async def delete_chat_session(db: AsyncSession, user_id: int, session_id: str):
        stmt = (
            select(ChatHistory)
            .where(
                ChatHistory.user_id == user_id,
                ChatHistory.session_id == uuid.UUID(session_id)
            )
        )
        cursor = await db.execute(stmt)
        messages = cursor.scalars().all()
        
        if not messages:
            raise HTTPException(status_code=404, detail="Session not found")
            
        for msg in messages:
            await db.delete(msg)
            
        await db.commit()
