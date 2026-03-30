"""
app/models/__init__.py

Re-exports all ORM models so that:
  1. Alembic `env.py` discovers every table via `Base.metadata`.
  2. `relationship()` back-references resolve without circular imports.
  3. Application code can do: `from app.models import User, JobCache`.
"""

from app.models.models import (  # noqa: F401
    # §2 Auth
    User,
    # §3 Profiles
    Profile,
    WorkExperience,
    Education,
    Certification,
    # §4 Skills
    Skill,
    UserSkill,
    # §5 Job Pipeline
    RawJob,
    Company,
    JobCache,
    # §6 ATS
    SavedJob,
    JobApplication,
    # §7 AI & Analytics
    ChatHistory,
    UserActivity,
    JobAlert,
    Notification,
    MarketInsightCache,
)

__all__ = [
    "User",
    "Profile",
    "WorkExperience",
    "Education",
    "Certification",
    "Skill",
    "UserSkill",
    "RawJob",
    "Company",
    "JobCache",
    "SavedJob",
    "JobApplication",
    "ChatHistory",
    "UserActivity",
    "JobAlert",
    "Notification",
    "MarketInsightCache",
]
