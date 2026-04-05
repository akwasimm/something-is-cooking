"""
models.py — Complete SQLAlchemy 2.0 ORM Models
================================================
Sections:
  §0  Enums
  §1  Shared Mixins
  §2  User & Authentication        — User
  §3  Complete User Profiles       — Profile, WorkExperience, Education, Certification
  §4  Skills & NLP Entities        — Skill, UserSkill
  §5  Job Pipeline & Companies     — RawJob, JobCache, Company
  §6  Application Tracking (ATS)   — SavedJob, JobApplication
  §7  AI Coach & Analytics         — ChatHistory, UserActivity, JobAlert,
                                     Notification, MarketInsightCache
"""

from __future__ import annotations

import enum
import uuid
from datetime import date, datetime
from typing import Any

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Enum as SAEnum,
    Float,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from app.core.database import Base


# ══════════════════════════════════════════════════════════════════════════════
# §0 — Enums
# ══════════════════════════════════════════════════════════════════════════════

class UserRole(str, enum.Enum):
    """Platform-level access-control role."""
    user = "user"
    admin = "admin"


class RemotePreference(str, enum.Enum):
    """Candidate's preferred work mode."""
    remote = "remote"
    onsite = "onsite"
    hybrid = "hybrid"
    any = "any"


class SkillProficiency(str, enum.Enum):
    """Self-assessed competency level on a particular skill."""
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"
    expert = "expert"


class ApplicationStatus(str, enum.Enum):
    """Full hiring-funnel lifecycle for a job application."""
    applied = "applied"
    viewed = "viewed"
    screening = "screening"
    interviewing = "interviewing"
    offered = "offered"
    rejected = "rejected"
    accepted = "accepted"
    withdrawn = "withdrawn"


class MessageType(str, enum.Enum):
    """Actor type for an AI chat message."""
    user = "user"
    assistant = "assistant"
    system = "system"


class AlertFrequency(str, enum.Enum):
    """How often a job alert is dispatched."""
    instant = "instant"
    daily = "daily"
    weekly = "weekly"


class EmploymentType(str, enum.Enum):
    """Work-experience employment contract type."""
    full_time = "full_time"
    part_time = "part_time"
    contract = "contract"
    freelance = "freelance"
    internship = "internship"
    apprenticeship = "apprenticeship"


# ══════════════════════════════════════════════════════════════════════════════
# §1 — Shared Mixins
# ══════════════════════════════════════════════════════════════════════════════

class TimestampMixin:
    """Adds server-managed `created_at` and `updated_at` columns."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
    )


class SoftDeleteMixin:
    """Adds `is_deleted` flag for soft-delete support."""

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


# ══════════════════════════════════════════════════════════════════════════════
# §2 — User & Authentication
# ══════════════════════════════════════════════════════════════════════════════

class User(TimestampMixin, Base):
    """
    Core authentication entity.

    Supports both email/password (password_hash) and OAuth flows
    (oauth_provider + oauth_id). A newly registered user begins with
    is_verified=False until they confirm their email.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    email: Mapped[str] = mapped_column(
        String(320),        # RFC 5321 maximum
        unique=True,
        nullable=False,
        index=True,
        comment="Primary login identifier — globally unique.",
    )
    password_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="bcrypt hash; NULL for OAuth-only accounts.",
    )
    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole, name="user_role", create_type=True),
        default=UserRole.user,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # OAuth (Google / GitHub / LinkedIn)
    oauth_provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
    oauth_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # ── Tokens (Auth & Recovery) ─────────────────────────────────
    refresh_token: Mapped[str | None] = mapped_column(
        String(500), nullable=True, comment="Persisted JWT refresh token."
    )
    reset_token: Mapped[str | None] = mapped_column(
        String(255), nullable=True, index=True, comment="Hashed password reset token."
    )
    reset_token_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # ── Relationships ────────────────────────────────────────────
    profile: Mapped["Profile | None"] = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    work_experiences: Mapped[list["WorkExperience"]] = relationship(
        "WorkExperience", back_populates="user", cascade="all, delete-orphan",
        order_by="WorkExperience.start_date.desc()",
    )
    educations: Mapped[list["Education"]] = relationship(
        "Education", back_populates="user", cascade="all, delete-orphan",
        order_by="Education.start_date.desc()",
    )
    certifications: Mapped[list["Certification"]] = relationship(
        "Certification", back_populates="user", cascade="all, delete-orphan",
    )
    skills: Mapped[list["UserSkill"]] = relationship(
        "UserSkill", back_populates="user", cascade="all, delete-orphan",
    )
    saved_jobs: Mapped[list["SavedJob"]] = relationship(
        "SavedJob", back_populates="user", cascade="all, delete-orphan",
    )
    applications: Mapped[list["JobApplication"]] = relationship(
        "JobApplication", back_populates="user", cascade="all, delete-orphan",
    )
    chat_histories: Mapped[list["ChatHistory"]] = relationship(
        "ChatHistory", back_populates="user", cascade="all, delete-orphan",
    )
    activities: Mapped[list["UserActivity"]] = relationship(
        "UserActivity", back_populates="user", cascade="all, delete-orphan",
    )
    job_alerts: Mapped[list["JobAlert"]] = relationship(
        "JobAlert", back_populates="user", cascade="all, delete-orphan",
    )
    notifications: Mapped[list["Notification"]] = relationship(
        "Notification", back_populates="user", cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("ix_users_oauth", "oauth_provider", "oauth_id"),
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r} role={self.role.value}>"


# ══════════════════════════════════════════════════════════════════════════════
# §3 — Complete User Profiles
# ══════════════════════════════════════════════════════════════════════════════

class Profile(Base):
    """
    Extended candidate profile — 1-to-1 with User.

    `profile_completion` (0–100) is computed by a background task
    and cached here so the UI can surface completion nudges without
    recalculating on every request.

    JSONB columns (`preferred_locations`, `job_type_preference`,
    `career_interests`) avoid extra junction tables for multi-value
    preferences while remaining queryable via PostgreSQL JSONB operators.
    """

    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    # ── Personal details ─────────────────────────────────────────
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    headline: Mapped[str | None] = mapped_column(String(220), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Media / Links ────────────────────────────────────────────
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    resume_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    linkedin_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    github_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    portfolio_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # ── Location ─────────────────────────────────────────────────
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    preferred_locations: Mapped[list[Any] | None] = mapped_column(
        JSONB, nullable=True,
        comment='e.g. ["London", "New York", "Remote"]',
    )

    # ── Career preferences ───────────────────────────────────────
    experience_years: Mapped[float | None] = mapped_column(Float, nullable=True)
    expected_salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    expected_salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    job_type_preference: Mapped[list[Any] | None] = mapped_column(
        JSONB, nullable=True,
        comment='e.g. ["full_time", "contract"]',
    )
    remote_preference: Mapped[RemotePreference | None] = mapped_column(
        SAEnum(RemotePreference, name="remote_preference", create_type=True),
        nullable=True,
    )
    notice_period: Mapped[str | None] = mapped_column(
        String(50), nullable=True,
        comment='e.g. "2 weeks", "1 month", "Immediately"',
    )
    career_interests: Mapped[list[Any] | None] = mapped_column(
        JSONB, nullable=True,
        comment='e.g. ["Machine Learning", "Backend Engineering"]',
    )

    # ── Gamification ─────────────────────────────────────────────
    profile_completion: Mapped[int] = mapped_column(
        SmallInteger, default=0, nullable=False,
        comment="0–100 percentage score computed by a background task.",
    )

    # ── AI / ML Embeddings ───────────────────────────────────────
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(384), nullable=True,
        comment="SBERT semantic embedding for candidate matching (384-dimensional)",
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    # ── Relationships ────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="profile")

    __table_args__ = (
        Index(
            "ix_profiles_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )

    def __repr__(self) -> str:
        return f"<Profile id={self.id} user_id={self.user_id}>"


class WorkExperience(TimestampMixin, Base):
    """
    Individual work-history entry for a user.

    `skills_used` is a JSONB array of skill names extracted by the NLP
    pipeline when the user pastes a job description, enabling automatic
    skill inference without manual tagging.
    """

    __tablename__ = "work_experiences"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )

    company_name: Mapped[str] = mapped_column(String(200), nullable=False)
    job_title: Mapped[str] = mapped_column(String(200), nullable=False)
    employment_type: Mapped[EmploymentType | None] = mapped_column(
        SAEnum(EmploymentType, name="employment_type", create_type=True),
        nullable=True,
    )
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    skills_used: Mapped[list[Any] | None] = mapped_column(
        JSONB, nullable=True,
        comment='NLP-extracted skill names, e.g. ["Python", "FastAPI", "Docker"]',
    )

    # ── Relationships ────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="work_experiences")

    def __repr__(self) -> str:
        return f"<WorkExperience id={self.id} user_id={self.user_id} title={self.job_title!r}>"


class Education(TimestampMixin, Base):
    """Academic qualification record."""

    __tablename__ = "educations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )

    institution: Mapped[str] = mapped_column(String(300), nullable=False)
    degree: Mapped[str | None] = mapped_column(
        String(200), nullable=True,
        comment='e.g. "Bachelor of Science", "Master of Engineering"',
    )
    field_of_study: Mapped[str | None] = mapped_column(String(200), nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    grade: Mapped[str | None] = mapped_column(String(50), nullable=True)
    activities: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Verification (Blockchain/Web3) ───────────────────────────
    verification_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_verified_on_chain: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # ── Relationships ────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="educations")

    def __repr__(self) -> str:
        return f"<Education id={self.id} user_id={self.user_id} institution={self.institution!r}>"


class Certification(TimestampMixin, Base):
    """Professional certification or licence held by a user."""

    __tablename__ = "certifications"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )

    name: Mapped[str] = mapped_column(String(300), nullable=False)
    issuing_organization: Mapped[str] = mapped_column(String(300), nullable=False)
    issue_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    credential_id: Mapped[str | None] = mapped_column(String(200), nullable=True)
    credential_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # ── Verification (Blockchain/Web3) ───────────────────────────
    verification_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_verified_on_chain: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # ── Relationships ────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="certifications")

    def __repr__(self) -> str:
        return f"<Certification id={self.id} name={self.name!r}>"


# ══════════════════════════════════════════════════════════════════════════════
# §4 — Skills & NLP Entities
# ══════════════════════════════════════════════════════════════════════════════

class Skill(TimestampMixin, Base):
    """
    Master skill catalogue populated and maintained by the NLP pipeline.

    `aliases` stores alternate spellings/abbreviations so the matching
    engine can resolve "JS" → "javascript", "ML" → "machine learning".
    `demand_score` is a float (0–1) updated weekly by frequency analysis
    over recent job postings and used to power the Trending Skills widget.
    """

    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True,
        comment="Canonical lowercase name, e.g. 'python', 'react', 'postgresql'.",
    )
    category: Mapped[str | None] = mapped_column(
        String(100), nullable=True,
        comment='e.g. "Programming Language", "Cloud Platform", "Framework".',
    )
    aliases: Mapped[list[Any] | None] = mapped_column(
        JSONB, nullable=True,
        comment='Alternate names for fuzzy matching, e.g. ["JS", "javascript"].',
    )
    is_trending: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    demand_score: Mapped[float | None] = mapped_column(
        Float, nullable=True,
        comment="0.0–1.0 score derived from recent job-posting frequency.",
    )

    # ── Relationships ────────────────────────────────────────────
    user_skills: Mapped[list["UserSkill"]] = relationship(
        "UserSkill", back_populates="skill", cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Skill id={self.id} name={self.name!r} trending={self.is_trending}>"


class UserSkill(Base):
    """
    Junction table: User ↔ Skill (many-to-many).

    `is_primary` flags the handful of core skills a user wants
    prominently displayed, separate from an exhaustive secondary list.
    """

    __tablename__ = "user_skills"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True,
    )
    skill_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True,
    )
    proficiency: Mapped[SkillProficiency] = mapped_column(
        SAEnum(SkillProficiency, name="skill_proficiency", create_type=True),
        default=SkillProficiency.intermediate,
        nullable=False,
    )
    years_of_exp: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
    )

    # ── Relationships ────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="skills")
    skill: Mapped["Skill"] = relationship("Skill", back_populates="user_skills")

    def __repr__(self) -> str:
        return (
            f"<UserSkill user_id={self.user_id} skill_id={self.skill_id} "
            f"proficiency={self.proficiency.value}>"
        )


# ══════════════════════════════════════════════════════════════════════════════
# §5 — Job Pipeline & Companies
# ══════════════════════════════════════════════════════════════════════════════

class RawJob(Base):
    """
    Append-only landing zone for scraped / imported job data.

    Accepts 100k+ records without any schema enforcement — the raw
    payload is stored as-is in JSONB. The NLP/ETL pipeline reads rows
    where `is_processed=False`, cleans them, deduplicates by
    `(source, source_id)`, and writes the result to `JobCache`.
    """

    __tablename__ = "raw_jobs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    raw_json_data: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False,
        comment="Full payload as received from the data source.",
    )
    source: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True,
        comment="Origin tag, e.g. 'linkedin', 'indeed', 'kaggle_dataset_v2'.",
    )
    source_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True,
        comment="Source-system job ID used to detect duplicates.",
    )
    is_processed: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, index=True,
    )
    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("source", "source_id", name="uq_raw_jobs_source_id"),
        Index("ix_raw_jobs_unprocessed", "is_processed", "ingested_at"),
    )

    def __repr__(self) -> str:
        return f"<RawJob id={self.id} source={self.source!r} processed={self.is_processed}>"


class Company(TimestampMixin, Base):
    """
    Deduplicated company master record.

    Culture ratings (0.0–5.0) are aggregated from user-submitted
    reviews and cached here. `is_verified` indicates that the company
    has claimed and validated their profile.
    """

    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        String(300), unique=True, nullable=False, index=True,
    )
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    linkedin_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    industry: Mapped[str | None] = mapped_column(String(150), nullable=True, index=True)
    company_size: Mapped[str | None] = mapped_column(
        String(50), nullable=True,
        comment='e.g. "1-10", "51-200", "1001-5000", "10000+".',
    )
    founded_year: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    headquarters: Mapped[str | None] = mapped_column(String(200), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Aggregated culture ratings (0.0–5.0)
    culture_rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    work_life_balance: Mapped[float | None] = mapped_column(Float, nullable=True)
    career_growth: Mapped[float | None] = mapped_column(Float, nullable=True)
    compensation: Mapped[float | None] = mapped_column(Float, nullable=True)

    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    job_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # ── Relationships ────────────────────────────────────────────
    jobs: Mapped[list["JobCache"]] = relationship("JobCache", back_populates="company_rel")

    def __repr__(self) -> str:
        return f"<Company id={self.id} name={self.name!r} verified={self.is_verified}>"


class JobCache(TimestampMixin, Base):
    """
    Refined, AI-ready job listing table — the primary search surface.

    Populated by the ETL pipeline after cleaning RawJob records.
    Keeping it separate from `raw_jobs` lets the pipeline regenerate or
    version records without affecting live search results.

    `skills_required` and `requirements` are JSONB for fast GIN-indexed
    containment queries: ``WHERE skills_required @> '["python"]'``.
    `is_description_generated=True` signals that an LLM synthesised
    the description from a sparse raw record.
    """

    __tablename__ = "job_cache"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    external_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    # ── Core fields ──────────────────────────────────────────────
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    company: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    company_logo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    company_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("companies.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    location: Mapped[str | None] = mapped_column(String(300), nullable=True, index=True)
    is_remote: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # ── Salary ───────────────────────────────────────────────────
    salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    is_salary_estimated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # ── Metadata ─────────────────────────────────────────────────
    job_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True,
        comment='e.g. "full_time", "contract", "internship".',
    )
    experience_level: Mapped[str | None] = mapped_column(
        String(50), nullable=True,
        comment='e.g. "entry", "mid", "senior", "lead".',
    )

    # ── Content ──────────────────────────────────────────────────
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    requirements: Mapped[list[Any] | None] = mapped_column(
        JSONB, nullable=True,
        comment="Structured bullet-point requirements extracted by NLP.",
    )
    skills_required: Mapped[list[Any] | None] = mapped_column(
        JSONB, nullable=True,
        comment='GIN-indexed skill array, e.g. ["python", "fastapi"].',
    )
    is_description_generated: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False,
    )

    # ── Integration & External Match ─────────────────────────────
    raw_data: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB, nullable=True,
        comment="Untouched JSON payloads from external job APIs",
    )
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(384), nullable=True,
        comment="SBERT semantic embedding for ML match pipeline (384-dimensional)",
    )

    apply_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    posted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True,
    )
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)

    # ── Relationships ────────────────────────────────────────────
    company_rel: Mapped["Company | None"] = relationship("Company", back_populates="jobs")
    saved_by: Mapped[list["SavedJob"]] = relationship(
        "SavedJob", back_populates="job", cascade="all, delete-orphan",
    )
    applications: Mapped[list["JobApplication"]] = relationship(
        "JobApplication", back_populates="job", cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uq_job_cache_source_external"),
        Index("ix_job_cache_active_posted", "is_active", "posted_at"),
        Index("ix_job_cache_skills_gin", "skills_required", postgresql_using="gin"),
        Index(
            "ix_job_cache_fulltext_gin",
            func.to_tsvector(
                "english",
                title
                + " "
                + company
                + " "
                + func.coalesce(description, "")
                + " "
                + func.cast(skills_required, Text),
            ),
            postgresql_using="gin",
        ),
        Index(
            "ix_job_cache_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )

    def __repr__(self) -> str:
        return f"<JobCache id={self.id} title={self.title!r} company={self.company!r}>"


# ══════════════════════════════════════════════════════════════════════════════
# §6 — Application Tracking System (ATS)
# ══════════════════════════════════════════════════════════════════════════════

class SavedJob(TimestampMixin, Base):
    """
    User-bookmarked / favourited job listing.

    `job_data` is a JSONB snapshot taken at save-time so the saved card
    remains intact even when the underlying `JobCache` row changes or
    is deactivated.
    `tags` allows users to label saved jobs (e.g. ["dream job", "apply this week"]).
    """

    __tablename__ = "saved_jobs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    job_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("job_cache.id", ondelete="SET NULL"),
        nullable=True, index=True,
    )
    external_job_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True,
        comment="Source-system ID for externally-applied jobs not in our DB.",
    )
    job_data: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB, nullable=True,
        comment="Point-in-time snapshot of the job at save time.",
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[list[Any] | None] = mapped_column(JSONB, nullable=True)

    # ── Relationships ────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="saved_jobs")
    job: Mapped["JobCache | None"] = relationship("JobCache", back_populates="saved_by")

    __table_args__ = (
        UniqueConstraint("user_id", "job_id", name="uq_saved_jobs_user_job"),
    )

    def __repr__(self) -> str:
        return f"<SavedJob id={self.id} user_id={self.user_id} job_id={self.job_id}>"


class JobApplication(TimestampMixin, Base):
    """
    Full end-to-end job application tracker.

    `interview_dates` is a JSONB array of ISO-8601 timestamps so
    multiple rounds can be tracked without extra tables.
    `salary_offered` is populated when status reaches "offered".
    `follow_up_date` powers the AI coach's proactive reminder nudges.
    """

    __tablename__ = "job_applications"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    job_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("job_cache.id", ondelete="SET NULL"),
        nullable=True, index=True,
    )
    external_job_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    job_data: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB, nullable=True,
        comment="Denormalised snapshot at application time.",
    )

    status: Mapped[ApplicationStatus] = mapped_column(
        SAEnum(ApplicationStatus, name="application_status", create_type=True),
        default=ApplicationStatus.applied,
        nullable=False,
        index=True,
    )
    applied_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
    )
    status_updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
    )

    resume_used: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cover_letter: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    follow_up_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    interview_dates: Mapped[list[Any] | None] = mapped_column(
        JSONB, nullable=True,
        comment='ISO-8601 timestamps for each interview round.',
    )
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    salary_offered: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # ── Relationships ────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="applications")
    job: Mapped["JobCache | None"] = relationship("JobCache", back_populates="applications")

    __table_args__ = (
        UniqueConstraint("user_id", "job_id", name="uq_applications_user_job"),
        Index("ix_applications_user_status", "user_id", "status"),
        Index("ix_applications_follow_up", "follow_up_date", "status"),
    )

    def __repr__(self) -> str:
        return (
            f"<JobApplication id={self.id} user_id={self.user_id} "
            f"job_id={self.job_id} status={self.status.value}>"
        )


# ══════════════════════════════════════════════════════════════════════════════
# §7 — AI Coach & Analytics (Premium Features)
# ══════════════════════════════════════════════════════════════════════════════

class ChatHistory(TimestampMixin, Base):
    """
    Persisted AI coach conversation messages.

    `session_id` groups messages into logical conversations. Using UUID
    prevents enumeration attacks on the session endpoint.
    `tokens_used` enables per-user token-budget enforcement for
    rate-limiting and cost accounting.
    `metadata` stores structured data attached to a message, such as
    job IDs referenced, resume sections discussed, or tool-call results.
    """

    __tablename__ = "chat_histories"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        nullable=False,
        index=True,
    )
    message_type: Mapped[MessageType] = mapped_column(
        SAEnum(MessageType, name="message_type", create_type=True),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_: Mapped[dict[str, Any] | None] = mapped_column(
        "metadata",          # column name in DB
        JSONB,
        nullable=True,
        comment="Structured payload attached to the message (tool calls, references, etc.).",
    )
    tokens_used: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # ── Relationships ────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="chat_histories")

    __table_args__ = (
        Index("ix_chat_session", "user_id", "session_id"),
    )

    def __repr__(self) -> str:
        return (
            f"<ChatHistory id={self.id} user_id={self.user_id} "
            f"session={self.session_id} type={self.message_type.value}>"
        )


class UserActivity(Base):
    """
    Behavioural event log for analytics and personalisation.

    Append-only — never updated after insert. Powers the recommendation
    engine (e.g. jobs viewed but not saved) and security audit trails.
    Partition by `created_at` monthly in production to manage table size.
    """

    __tablename__ = "user_activities"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    action_type: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True,
        comment='e.g. "job_viewed", "search_performed", "resume_downloaded".',
    )
    entity_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True,
        comment='e.g. "job", "company", "skill".',
    )
    entity_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    details: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True,
    )

    # ── Relationships ────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="activities")

    def __repr__(self) -> str:
        return (
            f"<UserActivity id={self.id} user_id={self.user_id} "
            f"action={self.action_type!r}>"
        )


class JobAlert(TimestampMixin, Base):
    """
    Saved job-search alert that triggers email / push notifications.

    `frequency` controls dispatch cadence. The alert worker queries
    `JobCache` using the stored filter parameters and sends only new
    matches since `last_sent`.
    """

    __tablename__ = "job_alerts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )

    alert_name: Mapped[str] = mapped_column(String(200), nullable=False)
    keywords: Mapped[list[Any] | None] = mapped_column(JSONB, nullable=True)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    job_type: Mapped[list[Any] | None] = mapped_column(JSONB, nullable=True)
    experience_level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)

    frequency: Mapped[AlertFrequency] = mapped_column(
        SAEnum(AlertFrequency, name="alert_frequency", create_type=True),
        default=AlertFrequency.daily,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_sent: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # ── Relationships ────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="job_alerts")

    def __repr__(self) -> str:
        return f"<JobAlert id={self.id} user_id={self.user_id} name={self.alert_name!r}>"


class Notification(TimestampMixin, Base):
    """
    In-app notification delivered to a user.

    `is_read` is toggled by the frontend when the user opens the
    notification centre. `link` is a relative URL the user is routed
    to on click (e.g. `/applications/42`).
    """

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    type: Mapped[str] = mapped_column(
        String(100), nullable=False,
        comment='e.g. "new_match", "application_update", "interview_reminder".',
    )
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)

    # ── Relationships ────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="notifications")

    __table_args__ = (
        Index("ix_notifications_unread", "user_id", "is_read"),
    )

    def __repr__(self) -> str:
        return (
            f"<Notification id={self.id} user_id={self.user_id} "
            f"type={self.type!r} read={self.is_read}>"
        )


class MarketInsightCache(Base):
    """
    Server-side cache for expensive AI-generated market insight reports.

    Computed blobs (salary bands, skill demand trends, hiring velocity)
    are stored here with a TTL (`expires_at`) so the API can serve
    pre-computed responses rather than running a full analysis per request.
    `parameters` captures the filter inputs (e.g. role, location, seniority)
    used to generate the insight so cache hits can be validated precisely.
    """

    __tablename__ = "market_insight_cache"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    insight_type: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True,
        comment='e.g. "salary_trend", "skill_demand", "hiring_velocity".',
    )
    parameters: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False,
        comment="Filter inputs used to generate this insight (for cache-key matching).",
    )
    data: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True,
    )

    __table_args__ = (
        Index("ix_insight_type_expires", "insight_type", "expires_at"),
    )

    def __repr__(self) -> str:
        return (
            f"<MarketInsightCache id={self.id} type={self.insight_type!r} "
            f"expires={self.expires_at}>"
        )
