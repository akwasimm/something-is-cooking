"""
Alembic migration: 002 — PostgreSQL Views
==========================================
Creates two read-only views used by the API and analytics dashboards:

  1. ``user_complete_profile``
       Joins users + profiles and aggregates user_skills into a JSON
       array. Used by the AI coach to load a full candidate snapshot
       in a single query.

  2. ``user_application_stats``
       Groups job_applications by user_id and counts each status bucket.
       Powers the ATS dashboard Stats cards without repeated GROUP BY
       queries in application code.

Revision ID : 002
Revises     : 001
"""

from alembic import op

# ── Revision identifiers ──────────────────────────────────────
revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


# ─────────────────────────────────────────────────────────────────────────────
# View DDL
# ─────────────────────────────────────────────────────────────────────────────

_VIEW_USER_COMPLETE_PROFILE = """
CREATE OR REPLACE VIEW user_complete_profile AS
SELECT
    u.id                        AS user_id,
    u.email,
    u.role,
    u.is_active,
    u.is_verified,
    u.last_login,
    u.created_at                AS member_since,

    -- Profile fields (NULL-safe via LEFT JOIN)
    p.first_name,
    p.last_name,
    p.phone,
    p.headline,
    p.summary,
    p.avatar_url,
    p.resume_url,
    p.linkedin_url,
    p.github_url,
    p.portfolio_url,
    p.location,
    p.preferred_locations,
    p.experience_years,
    p.expected_salary_min,
    p.expected_salary_max,
    p.salary_currency,
    p.job_type_preference,
    p.remote_preference,
    p.notice_period,
    p.career_interests,
    p.profile_completion,

    -- Aggregated skills as a JSON array of objects
    COALESCE(
        (
            SELECT json_agg(
                json_build_object(
                    'skill_id',    s.id,
                    'name',        s.name,
                    'category',    s.category,
                    'proficiency', us.proficiency,
                    'years',       us.years_of_exp,
                    'is_primary',  us.is_primary
                )
                ORDER BY us.is_primary DESC, s.name
            )
            FROM user_skills  us
            JOIN skills       s  ON s.id = us.skill_id
            WHERE us.user_id = u.id
        ),
        '[]'::json
    )                           AS skills

FROM users    u
LEFT JOIN profiles p ON p.user_id = u.id;
"""

_VIEW_USER_APPLICATION_STATS = """
CREATE OR REPLACE VIEW user_application_stats AS
SELECT
    user_id,
    COUNT(*)                                                    AS total_applications,
    COUNT(*) FILTER (WHERE status = 'applied')                  AS applied_count,
    COUNT(*) FILTER (WHERE status = 'viewed')                   AS viewed_count,
    COUNT(*) FILTER (WHERE status = 'screening')                AS screening_count,
    COUNT(*) FILTER (WHERE status = 'interviewing')             AS interviewing_count,
    COUNT(*) FILTER (WHERE status = 'offered')                  AS offered_count,
    COUNT(*) FILTER (WHERE status = 'rejected')                 AS rejected_count,
    COUNT(*) FILTER (WHERE status = 'accepted')                 AS accepted_count,
    COUNT(*) FILTER (WHERE status = 'withdrawn')                AS withdrawn_count,
    MAX(applied_at)                                             AS last_applied_at,
    -- Response rate: any status beyond 'applied' or 'viewed'
    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE status NOT IN ('applied', 'viewed', 'withdrawn')
        ) / NULLIF(COUNT(*), 0),
        2
    )                                                           AS response_rate_pct
FROM job_applications
GROUP BY user_id;
"""

# ── Drop DDL (for downgrade) ──────────────────────────────────

_DROP_USER_COMPLETE_PROFILE = "DROP VIEW IF EXISTS user_complete_profile;"
_DROP_USER_APPLICATION_STATS = "DROP VIEW IF EXISTS user_application_stats;"


# ─────────────────────────────────────────────────────────────────────────────
# Alembic hooks
# ─────────────────────────────────────────────────────────────────────────────

def upgrade() -> None:
    """Create the two PostgreSQL views."""
    op.execute(_VIEW_USER_COMPLETE_PROFILE)
    op.execute(_VIEW_USER_APPLICATION_STATS)


def downgrade() -> None:
    """Drop the views in reverse creation order."""
    op.execute(_DROP_USER_APPLICATION_STATS)
    op.execute(_DROP_USER_COMPLETE_PROFILE)
