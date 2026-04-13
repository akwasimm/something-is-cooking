"""
Alembic migration: 001 — Initial schema
=========================================
Creates all application tables in dependency order.

Revision ID : 001
Revises     : (none — base migration)
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS vector;')
    

    # ── users ───────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("email", sa.String(320), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=True),
        sa.Column("role", sa.Enum("user", "admin", name="user_role"), nullable=False, server_default="user"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("oauth_provider", sa.String(50), nullable=True),
        sa.Column("oauth_id", sa.String(255), nullable=True),
        sa.Column("last_login", sa.DateTime(timezone=True), nullable=True),
        sa.Column("refresh_token", sa.String(500), nullable=True),
        sa.Column("reset_token", sa.String(255), nullable=True),
        sa.Column("reset_token_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_oauth", "users", ["oauth_provider", "oauth_id"])
    op.create_index("ix_users_reset_token", "users", ["reset_token"])

    # ── profiles ───────────────────────────────────────────────
    op.create_table(
        "profiles",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False),
        sa.Column("first_name", sa.String(100), nullable=True),
        sa.Column("last_name", sa.String(100), nullable=True),
        sa.Column("phone", sa.String(30), nullable=True),
        sa.Column("headline", sa.String(220), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("avatar_url", sa.String(500), nullable=True),
        sa.Column("resume_url", sa.String(500), nullable=True),
        sa.Column("linkedin_url", sa.String(500), nullable=True),
        sa.Column("github_url", sa.String(500), nullable=True),
        sa.Column("portfolio_url", sa.String(500), nullable=True),
        sa.Column("location", sa.String(200), nullable=True),
        sa.Column("preferred_locations", JSONB, nullable=True),
        sa.Column("experience_years", sa.Float(), nullable=True),
        sa.Column("expected_salary_min", sa.Integer(), nullable=True),
        sa.Column("expected_salary_max", sa.Integer(), nullable=True),
        sa.Column("salary_currency", sa.String(3), nullable=False, server_default="USD"),
        sa.Column("job_type_preference", JSONB, nullable=True),
        sa.Column("remote_preference", sa.Enum("remote", "onsite", "hybrid", "any", name="remote_preference"), nullable=True),
        sa.Column("notice_period", sa.String(50), nullable=True),
        sa.Column("career_interests", JSONB, nullable=True),
        sa.Column("profile_completion", sa.SmallInteger(), nullable=False, server_default="0"),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_profiles_user_id", "profiles", ["user_id"])

    # ── work_experiences ────────────────────────────────────────
    op.create_table(
        "work_experiences",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("company_name", sa.String(200), nullable=False),
        sa.Column("job_title", sa.String(200), nullable=False),
        sa.Column("employment_type", sa.Enum("full_time", "part_time", "contract", "freelance", "internship", "apprenticeship", name="employment_type"), nullable=True),
        sa.Column("location", sa.String(200), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("is_current", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("skills_used", JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_work_experiences_user_id", "work_experiences", ["user_id"])

    # ── educations ─────────────────────────────────────────────
    op.create_table(
        "educations",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("institution", sa.String(300), nullable=False),
        sa.Column("degree", sa.String(200), nullable=True),
        sa.Column("field_of_study", sa.String(200), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("grade", sa.String(50), nullable=True),
        sa.Column("activities", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_educations_user_id", "educations", ["user_id"])

    # ── certifications ─────────────────────────────────────────
    op.create_table(
        "certifications",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(300), nullable=False),
        sa.Column("issuing_organization", sa.String(300), nullable=False),
        sa.Column("issue_date", sa.Date(), nullable=True),
        sa.Column("expiry_date", sa.Date(), nullable=True),
        sa.Column("credential_id", sa.String(200), nullable=True),
        sa.Column("credential_url", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_certifications_user_id", "certifications", ["user_id"])

    # ── skills ─────────────────────────────────────────────────
    op.create_table(
        "skills",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(100), unique=True, nullable=False),
        sa.Column("category", sa.String(100), nullable=True),
        sa.Column("aliases", JSONB, nullable=True),
        sa.Column("is_trending", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("demand_score", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_skills_name", "skills", ["name"], unique=True)

    # ── user_skills ────────────────────────────────────────────
    op.create_table(
        "user_skills",
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("skill_id", sa.Integer(), sa.ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("proficiency", sa.Enum("beginner", "intermediate", "advanced", "expert", name="skill_proficiency"), nullable=False, server_default="intermediate"),
        sa.Column("years_of_exp", sa.Float(), nullable=True),
        sa.Column("is_primary", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("added_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # ── raw_jobs ───────────────────────────────────────────────
    op.create_table(
        "raw_jobs",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("raw_json_data", JSONB, nullable=False),
        sa.Column("source", sa.String(100), nullable=False),
        sa.Column("source_id", sa.String(255), nullable=True),
        sa.Column("is_processed", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("ingested_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("source", "source_id", name="uq_raw_jobs_source_id"),
    )
    op.create_index("ix_raw_jobs_source", "raw_jobs", ["source"])
    op.create_index("ix_raw_jobs_unprocessed", "raw_jobs", ["is_processed", "ingested_at"])

    # ── companies ──────────────────────────────────────────────
    op.create_table(
        "companies",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(300), unique=True, nullable=False),
        sa.Column("logo_url", sa.String(500), nullable=True),
        sa.Column("website", sa.String(500), nullable=True),
        sa.Column("linkedin_url", sa.String(500), nullable=True),
        sa.Column("industry", sa.String(150), nullable=True),
        sa.Column("company_size", sa.String(50), nullable=True),
        sa.Column("founded_year", sa.SmallInteger(), nullable=True),
        sa.Column("headquarters", sa.String(200), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("culture_rating", sa.Float(), nullable=True),
        sa.Column("work_life_balance", sa.Float(), nullable=True),
        sa.Column("career_growth", sa.Float(), nullable=True),
        sa.Column("compensation", sa.Float(), nullable=True),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("job_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_companies_name", "companies", ["name"])
    op.create_index("ix_companies_industry", "companies", ["industry"])

    # ── job_cache ──────────────────────────────────────────────
    op.create_table(
        "job_cache",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("external_id", sa.String(255), nullable=True),
        sa.Column("source", sa.String(100), nullable=False),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("company", sa.String(300), nullable=False),
        sa.Column("company_logo", sa.String(500), nullable=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id", ondelete="SET NULL"), nullable=True),
        sa.Column("location", sa.String(300), nullable=True),
        sa.Column("is_remote", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("salary_min", sa.Integer(), nullable=True),
        sa.Column("salary_max", sa.Integer(), nullable=True),
        sa.Column("salary_currency", sa.String(3), nullable=False, server_default="USD"),
        sa.Column("is_salary_estimated", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("job_type", sa.String(50), nullable=True),
        sa.Column("experience_level", sa.String(50), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("requirements", JSONB, nullable=True),
        sa.Column("skills_required", JSONB, nullable=True),
        sa.Column("is_description_generated", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("apply_url", sa.String(1000), nullable=True),
        sa.Column("posted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("source", "external_id", name="uq_job_cache_source_external"),
    )
    op.create_index("ix_job_cache_title", "job_cache", ["title"])
    op.create_index("ix_job_cache_company", "job_cache", ["company"])
    op.create_index("ix_job_cache_location", "job_cache", ["location"])
    op.create_index("ix_job_cache_source", "job_cache", ["source"])
    op.create_index("ix_job_cache_active_posted", "job_cache", ["is_active", "posted_at"])
    op.create_index("ix_job_cache_skills_gin", "job_cache", ["skills_required"], postgresql_using="gin")

    # ── saved_jobs ─────────────────────────────────────────────
    op.create_table(
        "saved_jobs",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("job_id", sa.BigInteger(), sa.ForeignKey("job_cache.id", ondelete="SET NULL"), nullable=True),
        sa.Column("external_job_id", sa.String(255), nullable=True),
        sa.Column("job_data", JSONB, nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("tags", JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_id", "job_id", name="uq_saved_jobs_user_job"),
    )
    op.create_index("ix_saved_jobs_user_id", "saved_jobs", ["user_id"])
    op.create_index("ix_saved_jobs_job_id", "saved_jobs", ["job_id"])

    # ── job_applications ────────────────────────────────────────
    op.create_table(
        "job_applications",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("job_id", sa.BigInteger(), sa.ForeignKey("job_cache.id", ondelete="SET NULL"), nullable=True),
        sa.Column("external_job_id", sa.String(255), nullable=True),
        sa.Column("job_data", JSONB, nullable=True),
        sa.Column("status", sa.Enum("applied", "viewed", "screening", "interviewing", "offered", "rejected", "accepted", "withdrawn", name="application_status"), nullable=False, server_default="applied"),
        sa.Column("applied_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("status_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resume_used", sa.String(500), nullable=True),
        sa.Column("cover_letter", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("follow_up_date", sa.Date(), nullable=True),
        sa.Column("interview_dates", JSONB, nullable=True),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("salary_offered", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_id", "job_id", name="uq_applications_user_job"),
    )
    op.create_index("ix_applications_user_id", "job_applications", ["user_id"])
    op.create_index("ix_applications_job_id", "job_applications", ["job_id"])
    op.create_index("ix_applications_user_status", "job_applications", ["user_id", "status"])
    op.create_index("ix_applications_follow_up", "job_applications", ["follow_up_date", "status"])

    # ── chat_histories ─────────────────────────────────────────
    op.create_table(
        "chat_histories",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("session_id", UUID(as_uuid=True), nullable=False),
        sa.Column("message_type", sa.Enum("user", "assistant", "system", name="message_type"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("metadata", JSONB, nullable=True),
        sa.Column("tokens_used", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_chat_session", "chat_histories", ["user_id", "session_id"])

    # ── user_activities ────────────────────────────────────────
    op.create_table(
        "user_activities",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("action_type", sa.String(100), nullable=False),
        sa.Column("entity_type", sa.String(50), nullable=True),
        sa.Column("entity_id", sa.String(255), nullable=True),
        sa.Column("details", JSONB, nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_activities_user_id", "user_activities", ["user_id"])
    op.create_index("ix_activities_action_type", "user_activities", ["action_type"])
    op.create_index("ix_activities_created_at", "user_activities", ["created_at"])

    # ── job_alerts ─────────────────────────────────────────────
    op.create_table(
        "job_alerts",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("alert_name", sa.String(200), nullable=False),
        sa.Column("keywords", JSONB, nullable=True),
        sa.Column("location", sa.String(200), nullable=True),
        sa.Column("job_type", JSONB, nullable=True),
        sa.Column("experience_level", sa.String(50), nullable=True),
        sa.Column("salary_min", sa.Integer(), nullable=True),
        sa.Column("salary_max", sa.Integer(), nullable=True),
        sa.Column("frequency", sa.Enum("instant", "daily", "weekly", name="alert_frequency"), nullable=False, server_default="daily"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("last_sent", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_job_alerts_user_id", "job_alerts", ["user_id"])

    # ── notifications ──────────────────────────────────────────
    op.create_table(
        "notifications",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("type", sa.String(100), nullable=False),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("link", sa.String(500), nullable=True),
        sa.Column("is_read", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_notifications_user_id", "notifications", ["user_id"])
    op.create_index("ix_notifications_unread", "notifications", ["user_id", "is_read"])

    # ── market_insight_cache ────────────────────────────────────
    op.create_table(
        "market_insight_cache",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("insight_type", sa.String(100), nullable=False),
        sa.Column("parameters", JSONB, nullable=False),
        sa.Column("data", JSONB, nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_insight_type_expires", "market_insight_cache", ["insight_type", "expires_at"])


def downgrade() -> None:
    # Drop tables in reverse dependency order
    op.drop_table("market_insight_cache")
    op.drop_table("notifications")
    op.drop_table("job_alerts")
    op.drop_table("user_activities")
    op.drop_table("chat_histories")
    op.drop_table("job_applications")
    op.drop_table("saved_jobs")
    op.drop_table("job_cache")
    op.drop_table("companies")
    op.drop_table("raw_jobs")
    op.drop_table("user_skills")
    op.drop_table("skills")
    op.drop_table("certifications")
    op.drop_table("educations")
    op.drop_table("work_experiences")
    op.drop_table("profiles")
    op.drop_table("users")

    # Drop enums
    op.execute("DROP TYPE IF EXISTS alert_frequency")
    op.execute("DROP TYPE IF EXISTS message_type")
    op.execute("DROP TYPE IF EXISTS application_status")
    op.execute("DROP TYPE IF EXISTS skill_proficiency")
    op.execute("DROP TYPE IF EXISTS remote_preference")
    op.execute("DROP TYPE IF EXISTS employment_type")
    op.execute("DROP TYPE IF EXISTS user_role")
