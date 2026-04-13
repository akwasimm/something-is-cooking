# JobFor — Complete Codebase Documentation

> **Scope**: `jobfor/backend` (FastAPI Python API) + `jobfor/v2` (React frontend)
> **Generated**: 2026-04-13
> **Purpose**: Exhaustive reference for any developer or AI model to understand and work on this codebase without needing to read the source files.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Repository Layout](#2-repository-layout)
3. [Infrastructure & DevOps](#3-infrastructure--devops)
4. [Backend — Deep Dive](#4-backend--deep-dive)
   - 4.1 [Tech Stack & Dependencies](#41-tech-stack--dependencies)
   - 4.2 [Application Entry Point](#42-application-entry-point-mainpy)
   - 4.3 [Configuration System](#43-configuration-system)
   - 4.4 [Database Layer](#44-database-layer)
   - 4.5 [ORM Models (Complete Schema)](#45-orm-models-complete-schema)
   - 4.6 [API Routes](#46-api-routes)
   - 4.7 [Services Layer](#47-services-layer)
   - 4.8 [Background Tasks (Celery)](#48-background-tasks-celery)
   - 4.9 [Utilities & NLP](#49-utilities--nlp)
   - 4.10 [Data Seeding Scripts](#410-data-seeding-scripts)
5. [Frontend V2 — Deep Dive](#5-frontend-v2--deep-dive)
   - 5.1 [Tech Stack](#51-tech-stack)
   - 5.2 [Design System & Aesthetics](#52-design-system--aesthetics)
   - 5.3 [Application Routing](#53-application-routing)
   - 5.4 [Layout Architecture](#54-layout-architecture)
   - 5.5 [All Pages — Detailed Breakdown](#55-all-pages--detailed-breakdown)
   - 5.6 [Shared Components](#56-shared-components)
6. [Data Files](#6-data-files)
7. [Key Architectural Decisions](#7-key-architectural-decisions)
8. [Known Patterns & Conventions](#8-known-patterns--conventions)
9. [Current Limitations & TODOs](#9-current-limitations--todos)

---

## 1. Project Overview

**JobFor** is an AI-powered job search assistant platform targeting the Indian and global job market. It is a full-stack web application with two distinct parts:

| Part | Tech | Purpose |
|------|------|---------|
| `backend` | Python / FastAPI | REST API serving all data, AI, auth, and analytics |
| `v2` | React (Vite) | Modern, redesigned frontend UI (active development) |
| `frontend` | (older, skip) | Legacy frontend — not documented per user request |
| `data/` | JSON files | Seed data for the database |

**Core Value Propositions:**

- Intelligent job discovery powered by semantic search and ML-based recommendations
- AI Career Coach (GPT-4o-mini streaming chatbot) for resume, interview, salary advice
- Application Tracking System (ATS) with a Kanban board
- Market Insights: salary trends, skill demand analytics, company hiring data
- Resume upload + AI parsing to auto-populate user profile fields

---

## 2. Repository Layout

```
e:\Antigravity Projects\
└── jobfor/
    ├── backend/
    │   ├── main.py                     # App factory, CORS, lifespan hooks
    │   ├── requirements.txt
    │   ├── Dockerfile
    │   ├── alembic.ini
    │   ├── .env / .env.example
    │   ├── app/
    │   │   ├── api/
    │   │   │   ├── v1/
    │   │   │   │   ├── router.py       # Aggregates all endpoint routers
    │   │   │   │   └── endpoints/
    │   │   │   │       ├── auth.py
    │   │   │   │       ├── jobs.py
    │   │   │   │       ├── applications.py
    │   │   │   │       ├── ai_coach.py
    │   │   │   │       ├── insights.py
    │   │   │   │       ├── notifications.py
    │   │   │   │       ├── profile.py
    │   │   │   │       └── health.py
    │   │   │   └── dependencies/
    │   │   │       └── auth.py         # get_current_user JWT dependency
    │   │   ├── core/
    │   │   │   ├── config.py           # Pydantic settings (all env vars)
    │   │   │   ├── database.py         # Sync SQLAlchemy engine + Base
    │   │   │   ├── async_database.py   # Async asyncpg engine (used by all routes)
    │   │   │   ├── celery_app.py       # Celery worker + beat schedule
    │   │   │   ├── rate_limit.py       # SlowAPI limiter instance
    │   │   │   └── redis.py
    │   │   ├── models/
    │   │   │   ├── __init__.py
    │   │   │   └── models.py           # ALL ORM models (1523 lines)
    │   │   ├── schemas/                # Pydantic request/response schemas
    │   │   │   ├── auth.py
    │   │   │   ├── job.py
    │   │   │   ├── profile.py
    │   │   │   ├── ai_coach.py
    │   │   │   ├── insights.py
    │   │   │   ├── application.py
    │   │   │   └── notification.py
    │   │   ├── services/
    │   │   │   ├── auth_service.py
    │   │   │   ├── profile_service.py
    │   │   │   ├── job_service.py
    │   │   │   ├── recommendation_service.py
    │   │   │   ├── ai_coach_service.py
    │   │   │   ├── insights_service.py
    │   │   │   ├── application_service.py
    │   │   │   ├── cache_service.py
    │   │   │   ├── email_service.py
    │   │   │   ├── notification_service.py
    │   │   │   ├── scheduler_service.py
    │   │   │   └── nlp/
    │   │   │       ├── preprocessor.py
    │   │   │       └── skill_matcher.py
    │   │   └── utils/
    │   │       ├── security.py
    │   │       └── nlp_processor.py
    │   ├── migrations/
    │   └── scripts/
    │       ├── seed.py
    │       ├── seed_neon_db.py
    │       ├── ingest_jobs.py
    │       └── init_db.sql
    ├── v2/
    │   ├── index.html
    │   ├── package.json
    │   ├── vite.config.js
    │   ├── tailwind.config.js
    │   └── src/
    │       ├── main.jsx
    │       ├── App.jsx                 # Root router (all 18 routes)
    │       ├── index.css
    │       ├── components/
    │       │   ├── AppLayout.jsx
    │       │   ├── AppHeader.jsx
    │       │   ├── AppSidebar.jsx
    │       │   ├── PublicLayout.jsx
    │       │   ├── PublicNavbar.jsx
    │       │   ├── PublicFooter.jsx
    │       │   ├── Navbar.jsx
    │       │   ├── Footer.jsx
    │       │   ├── NeoButton.jsx
    │       │   └── SectionTitle.jsx
    │       └── [20 page files — see §5.5]
    ├── data/
    │   ├── companies.json
    │   ├── job_cache.json
    │   ├── skills.json
    │   └── market_insight_snapshots.json
    ├── docker-compose.yml
    └── indian-job-market-dataset-2025.xlsx   # Raw source (31 MB)
```

---

## 3. Infrastructure & DevOps

### Docker Compose

Three services defined in `docker-compose.yml`:

| Service | Image | Port | Role |
|---------|-------|------|------|
| `db` | `pgvector/pgvector:pg15` | 5432 | PostgreSQL 15 + pgvector extension |
| `redis` | `redis:7-alpine` | 6379 | Cache, Celery broker/backend, rate-limit counters |
| `backend` | Custom Dockerfile | 8000 | FastAPI via Uvicorn |

**Startup order**: `db` → `redis` → `backend` (enforced via `depends_on` health checks).

**Key details:**
- PostgreSQL and Redis data each persisted in named Docker volumes
- Redis uses AOF persistence + 256 MB max memory with LRU eviction
- Backend volume-mounts `./backend:/app` for hot-reload in development
- `init_db.sql` is auto-executed on PostgreSQL first-run to enable pgvector

### Running Locally (without Docker)

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend v2
cd v2
npm install
npm run dev   # http://localhost:5173
```

---

## 4. Backend — Deep Dive

### 4.1 Tech Stack & Dependencies

| Category | Library | Purpose |
|----------|---------|---------|
| API Framework | `fastapi ≥0.110` | REST API |
| ASGI Server | `uvicorn[standard]` | Production HTTP server |
| ORM | `sqlalchemy ≥2.0` | SQLAlchemy 2.0-style declarative ORM |
| DB Driver (sync) | `psycopg2-binary` | Used by Alembic + lifespan ping only |
| DB Driver (async) | `asyncpg` | Used by all FastAPI async routes |
| Migrations | `alembic` | Schema version control |
| Settings | `pydantic-settings` | Env var loading + type validation |
| Auth - Hashing | `passlib[bcrypt]` | Password hashing |
| Auth - JWT | `python-jose[cryptography]` | JWT creation and verification (HS256) |
| AI / LLM | `openai ≥1.30` | GPT-4o-mini API calls + streaming |
| Cache | `redis ≥5.0` | Redis client |
| Rate Limiting | `slowapi ≥0.1.9` | Per-route rate limits |
| Background Tasks | `celery[redis] ≥5.4` | Distributed task queue |
| NLP | `spacy ≥3.7` | Text processing pipeline |
| Fuzzy Matching | `rapidfuzz ≥3.6` | Skill alias resolution |
| ML | `scikit-learn`, `pandas`, `numpy` | TF-IDF recommendation engine |
| Data I/O | `openpyxl`, `xlrd` | Excel file ingestion |
| Email | `aiosmtplib ≥3.0` | Async SMTP |
| Vector Search | pgvector extension | SBERT embedding storage + HNSW similarity |
| Testing | `pytest`, `pytest-asyncio`, `httpx`, `factory-boy` | Unit/integration tests |

---

### 4.2 Application Entry Point (`main.py`)

`main.py` is the FastAPI application factory:

**1. Lifespan context manager** (startup/shutdown):
- Startup: calls `verify_connection()` → aborts if PostgreSQL unreachable; pings Redis → warns but continues if unavailable (rate limiting degrades gracefully).
- Shutdown: logs "shutting down gracefully".

**2. FastAPI app** with:
- `title`, `version` from `settings`
- OpenAPI + Docs URLs under `/api/v1`
- Custom contact and license metadata

**3. CORS Middleware** — Allows `http://localhost:5173` and `http://localhost:3000` by default. Configurable via `ALLOWED_ORIGINS` env var (JSON string or list).

**4. Rate Limiting** — SlowAPI limiter attached to `app.state.limiter`. `RateLimitExceeded` handled by SlowAPI's built-in handler.

**5. Global Exception Handlers:**

| Exception | Response |
|-----------|----------|
| `HTTPException` | `{success: false, error: detail, status_code}` |
| `Exception` (catch-all) | 500 — never leaks traceback |

**6. Routers** — single `api_router` mounted at prefix `/api/v1`

**7. Root Endpoints:**
- `GET /` — liveness probe (no DB I/O)
- `GET /health` — deep health check (PostgreSQL + Redis ping)

---

### 4.3 Configuration System

**File**: `app/core/config.py`

Single Pydantic-settings `Settings` class reading `.env`. Accessed everywhere as:
```python
from app.core.config import settings
```

| Group | Key Variables | Notes |
|-------|--------------|-------|
| **App** | `PROJECT_NAME`, `VERSION`, `API_V1_STR="/api/v1"` | |
| **Security** | `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES=1440`, `REFRESH_TOKEN_EXPIRE_DAYS=30` | Default key is insecure placeholder |
| **PostgreSQL** | `POSTGRES_USER/PASSWORD/DB/HOST/PORT`, `DATABASE_URL` | `DATABASE_URL` takes precedence (used for Neon) |
| **Redis** | `REDIS_HOST/PORT/PASSWORD/DB`, `UPSTASH_REDIS_REST_URL/TOKEN` | |
| **CORS** | `ALLOWED_ORIGINS` | JSON string or list |
| **OpenAI** | `OPENAI_API_KEY`, `OPENAI_MODEL="gpt-4o-mini"`, `OPENAI_MAX_TOKENS=2048`, `OPENAI_TEMPERATURE=0.7`, `AI_DAILY_TOKEN_BUDGET=100000` | |
| **Email** | `SMTP_HOST/PORT/USER/PASSWORD`, `EMAILS_FROM_EMAIL/NAME` | |
| **S3/MinIO** | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `S3_BUCKET_NAME`, `AWS_ENDPOINT_URL` | |
| **Celery** | `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND` | Both defaulting to Redis DB 1 and DB 2 |
| **External APIs** | `ADZUNA_APP_ID/KEY`, `RAPIDAPI_KEY` | For job syncing |
| **Rate Limiting** | `RATE_LIMIT_PER_MINUTE=60` | |

**`DB_URL` property**: Returns `DATABASE_URL` if set, otherwise assembles `postgresql+psycopg2://user:pass@host:port/db`.

**`REDIS_URL` property**: Assembles `redis://:password@host:port/db`.

---

### 4.4 Database Layer

Two database modules coexist:

#### `app/core/database.py` — Synchronous Engine

- **Used by**: Alembic, `verify_connection()` in lifespan, `db_session()` context manager for scripts and Celery workers
- Engine: `pool_size=10`, `max_overflow=20`, `pool_recycle=1800`, `pool_pre_ping=True`
- Session factory: `SessionLocal` with `autocommit=False`, `autoflush=False`, `expire_on_commit=False`
- SQLite compatibility shim for unit tests (WAL mode + foreign keys)
- `Base` — the `DeclarativeBase` all models inherit from
- `get_db()` — FastAPI sync dependency (rarely used; async is preferred)
- `init_db()` — creates all tables from `Base.metadata`
- `verify_connection()` — executes `SELECT 1`, returns bool

#### `app/core/async_database.py` — Async Engine (Primary)

- **Used by**: ALL FastAPI async route handlers
- Driver: `asyncpg` (`postgresql+asyncpg://`)
- URL builder: strips existing driver prefix from `DATABASE_URL` and re-attaches `asyncpg`
- Same pool settings as sync
- Session factory: `AsyncSessionLocal` (async_sessionmaker)
- `get_async_db()` — FastAPI async dependency; auto-commits on success, rolls back on exception
- `async_db_session()` — async context manager for Celery tasks and scripts

---

### 4.5 ORM Models (Complete Schema)

All models live in `app/models/models.py` (1523 lines). Organized into 9 sections.

#### Enums

| Enum | Values |
|------|--------|
| `UserRole` | `user`, `admin` |
| `RemotePreference` | `remote`, `onsite`, `hybrid`, `any` |
| `SkillProficiency` | `beginner`, `intermediate`, `advanced`, `expert` |
| `ApplicationStatus` | `applied`, `viewed`, `screening`, `interviewing`, `offered`, `rejected`, `accepted`, `withdrawn` |
| `MessageType` | `user`, `assistant`, `system` |
| `AlertFrequency` | `instant`, `daily`, `weekly` |
| `EmploymentType` | `full_time`, `part_time`, `contract`, `freelance`, `internship`, `apprenticeship` |

#### Mixins

- **`TimestampMixin`**: `created_at` (server_default `now()`), `updated_at` (auto `onupdate`)
- **`SoftDeleteMixin`**: `is_deleted` (Boolean), `deleted_at` (DateTime)

---

#### §2 — `User` (`users` table)

| Column | Type | Notes |
|--------|------|-------|
| `id` | BigInteger PK | Auto-increment |
| `email` | String(320) unique indexed | RFC 5321 max |
| `password_hash` | String(255) nullable | bcrypt; NULL for OAuth-only accounts |
| `role` | Enum(UserRole) | Default `user` |
| `is_active` | Boolean | Default True |
| `is_verified` | Boolean | False until email confirmed |
| `oauth_provider` | String(50) nullable | e.g. "google", "github" |
| `oauth_id` | String(255) nullable | OAuth sub |
| `last_login` | DateTime nullable | |
| `refresh_token` | String(500) nullable | Persisted JWT; nulled on logout |
| `reset_token` | String(255) nullable indexed | SHA-256 hash of reset token |
| `reset_token_expires_at` | DateTime nullable | 1-hour TTL |

**Composite index**: `(oauth_provider, oauth_id)`

**Relationships (all cascade `all, delete-orphan`)**:
`profile` (1:1, lazy=selectin), `work_experiences`, `educations`, `certifications`, `skills` (UserSkill), `saved_jobs`, `applications`, `chat_histories`, `activities`, `job_alerts`, `notifications`, `resumes`, `job_collections`, `ai_recommendations`, `ai_coach_tips`, `resume_analyses`

---

#### §3 — `Profile` (`profiles` table) — 1:1 with User

| Column | Type | Notes |
|--------|------|-------|
| `first_name`, `last_name` | String(100) nullable | |
| `phone` | String(30) nullable | |
| `headline` | String(220) nullable | LinkedIn-style tagline |
| `summary` | Text nullable | Professional bio |
| `avatar_url`, `resume_url`, `linkedin_url`, `github_url`, `portfolio_url` | String(500) nullable | |
| `location` | String(200) nullable | |
| `preferred_locations` | JSONB nullable | `["London", "Remote"]` |
| `experience_years` | Float nullable | |
| `expected_salary_min`, `expected_salary_max` | Integer nullable | |
| `salary_currency` | String(3) | Default "USD" |
| `job_type_preference` | JSONB nullable | `["full_time", "contract"]` |
| `remote_preference` | Enum(RemotePreference) nullable | |
| `notice_period` | String(50) nullable | e.g. "2 weeks" |
| `career_interests` | JSONB nullable | Topic interests |
| `target_roles` | JSONB nullable | Preferred job titles |
| `profile_completion` | SmallInteger | 0–100, computed score |
| `embedding` | Vector(384) nullable | SBERT embedding for candidate matching |

**HNSW index** on `embedding` column: `m=16, ef_construction=64, vector_cosine_ops`

---

#### §3 continued — `WorkExperience`, `Education`, `Certification`

**`WorkExperience`** (`work_experiences`):
`company_name`, `job_title`, `employment_type`, `location`, `start_date`, `end_date`, `is_current`, `description`, `skills_used` (JSONB — NLP extracted skills array)

**`Education`** (`educations`):
`institution`, `degree`, `field_of_study`, `start_date`, `end_date`, `grade`, `activities`, `verification_hash`, `is_verified_on_chain` (blockchain-ready stubs)

**`Certification`** (`certifications`):
`name`, `issuing_organization`, `issue_date`, `expiry_date`, `credential_id`, `credential_url`, `verification_hash`, `is_verified_on_chain`

---

#### §4 — Skills

**`Skill`** (`skills`) — Master catalogue:

| Column | Notes |
|--------|-------|
| `name` | Canonical lowercase, unique, indexed |
| `category` | e.g. "Programming Language" |
| `aliases` | JSONB — `["JS", "javascript"]` for fuzzy matching |
| `is_trending` | Boolean |
| `demand_score` | Float 0.0–1.0, updated weekly |

**`UserSkill`** (`user_skills`) — Junction User ↔ Skill:

| Column | Notes |
|--------|-------|
| `user_id`, `skill_id` | Composite PK |
| `proficiency` | Enum(SkillProficiency), default `intermediate` |
| `years_of_exp` | Float nullable |
| `is_primary` | Boolean — flagged for prominent display |

---

#### §5 — Job Pipeline

**`RawJob`** (`raw_jobs`) — Append-only ETL landing zone:
- `raw_json_data` (JSONB) — untouched payload
- `source` — origin tag (e.g. "linkedin", "kaggle_dataset_v2")
- `is_processed` (Boolean, indexed) — pickup flag for ETL
- Unique constraint: `(source, source_id)`
- Compound index: `(is_processed, ingested_at)`

**`Company`** (`companies`) — Deduplicated master:
`name` (unique), `logo_url`, `website`, `linkedin_url`, `industry`, `company_size`, `founded_year`, `headquarters`, `description`, `culture_rating`, `work_life_balance`, `career_growth`, `compensation` (all Float 0.0–5.0), `is_verified`, `job_count`

**`JobCache`** (`job_cache`) — **Primary search surface** (most important table):

| Column | Type | Notes |
|--------|------|-------|
| `external_id` | String(255) | Source-system ID |
| `source` | String(100) indexed | Origin tag |
| `title` | String(300) | |
| `company` | String(300) indexed | |
| `company_id` | FK → companies nullable | SET NULL on delete |
| `location` | String(300) nullable indexed | |
| `is_remote` | Boolean | |
| `salary_min`, `salary_max` | Integer nullable | |
| `salary_currency` | String(3) | Default "USD" |
| `is_salary_estimated` | Boolean | |
| `job_type` | String(50) | e.g. "full_time" |
| `experience_level` | String(50) | e.g. "senior" |
| `description` | Text nullable | |
| `requirements` | JSONB | NLP-extracted bulletpoints |
| `skills_required` | JSONB | **GIN-indexed** skill array |
| `is_description_generated` | Boolean | True if LLM synthesised description |
| `raw_data` | JSONB nullable | Untouched external API payload |
| `embedding` | Vector(384) nullable | **SBERT embedding for vector search** |
| `apply_url` | String(1000) nullable | |
| `posted_at` | DateTime nullable indexed | |
| `expires_at` | DateTime nullable | |
| `is_active` | Boolean indexed | |

**Indexes on `job_cache`**:
- `(is_active, posted_at)` — timeline queries
- `skills_required` — GIN for containment `WHERE skills_required @> '["python"]'`
- Full-text GIN: `to_tsvector('english', title || company || description || skills_cast)`
- HNSW on `embedding`: `m=16, ef_construction=64, vector_cosine_ops`

**Unique constraint**: `(source, external_id)`

---

#### §6 — ATS (Application Tracking System)

**`SavedJob`** (`saved_jobs`):

| Column | Notes |
|--------|-------|
| `user_id`, `job_id` | `job_id` nullable (SET NULL if job deleted) |
| `job_data` | JSONB snapshot at save time (preserved even if job deactivated) |
| `notes`, `tags` | User annotations |
| `match_score` | SmallInteger 0–100 cached at save time |
| `collection_id` | FK → job_collections nullable |

Unique constraint: `(user_id, job_id)`

**`JobApplication`** (`job_applications`):

| Column | Notes |
|--------|-------|
| `status` | Enum(ApplicationStatus) |
| `applied_at` | Server default |
| `resume_used`, `cover_letter`, `notes`, `feedback` | Text fields |
| `follow_up_date` | AI Coach reminder trigger |
| `interview_dates` | JSONB — ISO-8601 timestamps per round |
| `salary_offered` | Integer nullable |
| **`kanban_column`** | e.g. "applied", "interviewing", "offered", "closed" |
| **`kanban_position`** | SmallInteger — drag-drop sort order within column |
| `status_label` | Human-readable display text |
| `status_icon` | Material Symbols icon name |
| `time_label`, `time_label_bg`, `time_label_color` | Pill rendering config |

Indexes: `(user_id, status)`, `(follow_up_date, status)`, `(user_id, kanban_column, kanban_position)`

---

#### §7 — AI Coach & Analytics

**`ChatHistory`** (`chat_histories`):

| Column | Notes |
|--------|-------|
| `session_id` | UUID — groups messages into conversations |
| `message_type` | Enum(MessageType): user / assistant / system |
| `content` | Text |
| `metadata_` | JSONB (DB column name: `metadata`) — tool calls, refs, etc. |
| `tokens_used` | Integer nullable — cost tracking |

Index: `(user_id, session_id)`

**`UserActivity`** (`user_activities`) — Append-only event log:
`action_type` (e.g. "job_viewed"), `entity_type`, `entity_id`, `details` (JSONB), `ip_address`, `user_agent`

**`JobAlert`** (`job_alerts`) — Saved search alerts:
`alert_name`, `keywords` (JSONB), `location`, `job_type` (JSONB), `experience_level`, `salary_min/max`, `frequency` (Enum), `last_sent` (used for lookback window)

**`Notification`** (`notifications`):
`type` (e.g. "JOB_ALERT"), `title`, `message`, `link`, `is_read`, `read_at`

**`MarketInsightCache`** (`market_insight_caches`):
`insight_type` (e.g. "salary_trend"), `parameters` (JSONB), `data` (JSONB), `expires_at` — 24-hour TTL

---

#### §8 & §9 — User Assets & AI Extras

**`UserResume`**: Resume file records — `filename`, `storage_url`, `file_size`, `is_primary`, `parsed_data` (JSONB)

**`JobCollection`**: Named saved-job groups — `name`, `description`, `color`, `icon`, `is_default`

**`AIJobRecommendation`**: Cached ML recommendation per user+job — `match_score`, `match_breakdown` (JSONB)

**`AICoachTip`**: Saved AI tips — `category`, `content`, `is_saved`, `session_id`

**`ResumeAnalysis`**: AI resume review results — `overall_score`, `ats_score`, `strengths`, `improvements`, `suggestions` (JSONB arrays), `raw_analysis`

---

### 4.6 API Routes

All routes are prefixed `/api/v1`. The router is assembled in `app/api/v1/router.py`.

#### Auth (`/auth`)

| Method | Path | Auth? | Description |
|--------|------|-------|-------------|
| POST | `/auth/register` | No | Creates User + Profile, returns JWT pair |
| POST | `/auth/login` | No | Email + password → JWT pair |
| POST | `/auth/refresh` | No | Refresh token → new access + refresh tokens |
| POST | `/auth/logout` | Yes | Nulls refresh_token in DB |
| GET | `/auth/me` | Yes | Returns current user from JWT |
| POST | `/auth/forgot-password` | No | Generates reset token; silent 202 (anti-enumeration) |
| POST | `/auth/reset-password` | No | Validates token hash, updates password |
| GET | `/auth/google` | No | Placeholder — OAuth not implemented |
| GET | `/auth/github` | No | Placeholder — OAuth not implemented |

#### Jobs (`/jobs`)

| Method | Path | Auth? | Description |
|--------|------|-------|-------------|
| GET | `/jobs/search` | No | Full-text + filter search, paginated |
| GET | `/jobs/trending` | No | Top recent jobs by `posted_at` |
| GET | `/jobs/user/recommendations` | Yes | Hybrid ML recommendations for current user |
| GET | `/jobs/{job_id}` | No | Single job full details |
| GET | `/jobs/{job_id}/similar` | No | Jaccard-based similar jobs |

#### Profile (`/profile`)

| Method | Path | Auth? | Description |
|--------|------|-------|-------------|
| GET | `/profile/me` | Yes | Full profile with all nested data |
| PUT | `/profile/me` | Yes | Update profile fields (partial) |
| POST | `/profile/me/resume` | Yes | Upload PDF → GPT parsing → auto-fill profile |
| POST/PUT/DELETE | `/profile/work-experience/...` | Yes | Work experience CRUD |
| POST/PUT/DELETE | `/profile/education/...` | Yes | Education CRUD |
| POST/PUT/DELETE | `/profile/certification/...` | Yes | Certification CRUD |

#### AI Coach (`/ai-coach`)

| Method | Path | Rate Limit | Auth? | Description |
|--------|------|-----------|-------|-------------|
| POST | `/ai-coach/chat` | 20/hour | Yes | Streaming SSE chat (GPT-4o-mini generator) |
| POST | `/ai-coach/resume-review` | — | Yes | JSON resume analysis |
| POST | `/ai-coach/cover-letter` | — | Yes | Cover letter (2 variants) |
| POST | `/ai-coach/interview-prep` | — | Yes | Q&A + STAR scenarios |
| POST | `/ai-coach/salary-negotiation` | — | Yes | Tactical advice + email template |
| POST | `/ai-coach/career-path` | — | Yes | Career transition roadmap |
| GET | `/ai-coach/sessions` | — | Yes | List conversation sessions |
| GET | `/ai-coach/sessions/{id}` | — | Yes | Full chat history for session |
| DELETE | `/ai-coach/sessions/{id}` | — | Yes | Delete session (204) |

#### Market Insights (`/insights`)

| Method | Path | Auth? | Description |
|--------|------|-------|-------------|
| GET | `/insights/salary?role=&location=` | Yes | Salary min/median/max |
| GET | `/insights/skills/demand?limit=20` | Yes | Top skills by demand % |
| GET | `/insights/skill-gap?role=` | Yes | Gap vs. market + AI learning path |
| GET | `/insights/companies?limit=20` | Yes | Companies ranked by job count |

#### Notifications (`/notifications`)

CRUD for `Notification` and `JobAlert` records, plus marking notifications as read.

#### Applications (`/applications`)

Full ATS CRUD + kanban position updates + stats aggregation by status.

#### Health (`/health`)

`GET /health` → `{"status": "ok"}`

---

### 4.7 Services Layer

All services receive `AsyncSession` and encapsulate all business logic, keeping route handlers thin.

#### `AuthService` (class, instantiated per-request)

- **`register(user_in)`** — Checks email uniqueness (HTTP 409 if taken), bcrypt-hashes password, creates `User`, `await db.flush()` to get PK, creates `Profile`, generates JWT pair, commits.
- **`login(login_in)`** — Email lookup, bcrypt verify, updates `last_login`, generates JWT pair.
- **`refresh_token(token)`** — Decodes refresh JWT with python-jose, validates against DB-stored token (enables revocation), rotates token pair.
- **`logout(user_id)`** — Sets `refresh_token = None` and commits.
- **`request_password_reset(email)`** — `secrets.token_urlsafe(32)` → stores SHA-256 hash + 1hr expiry. Logs reset URL (email not actually sent currently).
- **`reset_password(token, new_password)`** — Validates hashed token, updates bcrypt hash, nulls `reset_token` and `refresh_token`.

**JWT utilities** (`app/utils/security.py`):
- `create_access_token(subject)` → HS256 JWT, expires `ACCESS_TOKEN_EXPIRE_MINUTES`
- `create_refresh_token(subject)` → HS256 JWT, expires `REFRESH_TOKEN_EXPIRE_DAYS` days
- `verify_password(plain, hashed)` → passlib bcrypt verify
- `get_password_hash(password)` → passlib bcrypt hash

**Auth dependency** (`app/api/dependencies/auth.py`):
`get_current_user` — pulls `Authorization: Bearer <token>`, decodes HS256, loads `User` from DB. Raises HTTP 401 on any failure.

---

#### `ProfileService` (class, instantiated per-request)

- **`get_profile(user_id)`** — Eager-loads `work_experiences`, `educations`, `certifications` via `selectinload`. Raises 404 if not found.
- **`update_profile(user_id, data)`** — `model_dump(exclude_unset=True)` for partial updates. Converts HttpUrl fields to strings.
- **Work Exp / Education / Cert CRUD** — Standard create/update/delete with user ownership validation.
- **`upload_and_parse_resume(user_id, file)`**:
  1. Saves PDF to `uploads/` directory
  2. Extracts text via `nlp_processor.extract_text_from_pdf()`
  3. GPT-4o-mini structured JSON extraction (name, phone, summary, skills, work exp, education)
  4. Creates `Skill` + `UserSkill` records for extracted skills
  5. Creates `WorkExperience` + `Education` records
  6. Recalculates `profile_completion` score
- **`_calculate_profile_completion(profile)`** → Weighted: name(15), headline/summary(20), phone(10), location(5), resume_url(20), work_exp(15), education(10), skills(5) = max 100

---

#### `JobService` (static methods)

- **`search_jobs(db, params)`** — Dynamic filter construction on `JobCache` using `JobSearchParams` (keyword ILIKE on title/company/description, location ILIKE, is_remote, job_type, experience_level, salary range). Returns `PaginatedJobResponse`.
- **`get_trending_jobs(db, limit)`** — `ORDER BY posted_at DESC WHERE is_active=True`
- **`get_job_by_id(db, job_id)`** — Single job or 404
- **`get_similar_jobs(db, job_id, limit)`** — Finds target job's skills, queries other active jobs with skill overlaps via JSONB containment

---

#### `RecommendationService` — Hybrid ML Engine (static methods)

Five scoring signals combined with weights:

| Signal | Weight | Algorithm |
|--------|--------|-----------|
| Skill match | **35%** | Jaccard — `len(intersection) / len(union)` on skill sets |
| Content match | **25%** | scikit-learn TF-IDF cosine similarity (profile text vs. job text) |
| Experience match | **15%** | Heuristic: years-of-exp → entry/mid/senior/director levels |
| Location match | **15%** | Substring match or remote preference check |
| Salary match | **10%** | `expected_min ≤ job_max` with 20%/40% decay bands |

**`get_recommendations(db, user_id, limit)`** flow:
1. Fetch user profile + eager-load skills + work experiences
2. Build TF-IDF corpus from user text
3. Fetch all active jobs
4. For each job: compute all 5 scores → weighted sum × 100
5. Reject scores < 40 (threshold filter)
6. Sort descending → return top `limit` with `match_breakdown` dict

---

#### `AiCoachService` — GPT-4o-mini Integration (static methods)

All methods use `AsyncOpenAI(api_key=settings.OPENAI_API_KEY)`.

- **`chat(...)` (async generator — SSE streaming)**:
  1. Resolves or creates session UUID
  2. Loads user profile (skills + work exp) → builds context string
  3. Loads prior messages for session from `chat_histories`
  4. Assembles OpenAI messages array: system (with context), history, new user message
  5. Streams response chunks → `yield text_blob` for SSE
  6. After streaming ends, persists both user + assistant messages to DB

- **`review_resume()`** → JSON: `{overallScore, strengths, improvements, suggestions, atsScore}`
- **`generate_cover_letter()`** → JSON: `{primary_letter, alternative_variation}`
- **`interview_prep()`** → JSON: `{common_questions, star_scenarios, tips}`
- **`salary_negotiation()`** → JSON: `{market_benchmark, counter_offer_strategies, email_template}`
- **`career_path()`** → JSON: `{milestones, recommended_skills, resources}`
- **`get_chat_sessions()`** → Groups `ChatHistory` by `session_id`, returns session summaries
- **`delete_chat_session()`** → Deletes all messages for a session; 404 if session not found

---

#### `InsightsService` — Analytics with DB Cache (static methods)

All methods check `MarketInsightCache` first (24-hour TTL), compute if miss, write result to cache.

- **`get_salary_insights(db, role, location)`** → Filters `JobCache` by role title ILIKE + location ILIKE → aggregates salary values → computes min/median/max using Python `statistics.median`
- **`get_skill_demand(db, limit)`** → Fetches all `skills_required` JSONB arrays → counts frequencies → returns top `limit` with `demandPercentage = (count/total_jobs)*100`
- **`analyze_skill_gap(db, user_id, target_role)`**:
  1. Loads user skills
  2. Fetches top 15 skills from jobs for target role
  3. Categorizes: strong (have), improve (missing, demand <30%), critical (missing, demand ≥30%)
  4. Computes `readinessScore` as weighted match %
  5. Calls GPT-4o-mini for 4-week learning roadmap for critical missing skills
- **`get_company_insights(db, limit)`** → Groups `JobCache` by company, counts active jobs, flags `isMassHiring` if ≥20 jobs

---

#### `SchedulerService` — Celery Tasks

**`sync_external_jobs()`** (hourly):
1. Async HTTP calls to Adzuna and JSearch (RapidAPI) concurrently via `httpx.AsyncClient`
2. Maps both responses to `JobCache` objects
3. Upserts: checks `external_id` existence, inserts new records

**`process_job_alerts()`** (midnight + noon):
1. Fetches all active `JobAlert` records
2. Computes lookback window from `frequency` (instant=1hr, daily=24hr, weekly=168hr)
3. Queries `JobCache` with alert's keyword, location, salary filters
4. Creates `Notification` records, updates `alert.last_sent`
5. Sends email via `email_service`

---

### 4.8 Background Tasks (Celery)

**`app/core/celery_app.py`**:
- Broker: Redis DB 1
- Backend: Redis DB 2
- Includes: `app.services.scheduler_service`
- Serializer: JSON, UTC timezone, task time limit 3600s

**Beat Schedule**:
```python
"sync-jobs-hourly"           → crontab(minute=0)         # Every hour
"process-alerts-twice-daily" → crontab(minute=0, hour="0,12")  # Midnight + noon
```

**Starting Celery**:
```bash
celery -A app.core.celery_app worker --loglevel=info
celery -A app.core.celery_app beat --loglevel=info
```

---

### 4.9 Utilities & NLP

**`app/utils/security.py`**: JWT (python-jose HS256), passlib bcrypt. Constants: `SECRET_KEY`, `ALGORITHM = "HS256"`.

**`app/utils/nlp_processor.py`**: `extract_text_from_pdf(file_bytes)` — PDF → plain text (used in resume upload).

**`app/services/nlp/preprocessor.py`**: Text cleaning, stop word removal, tokenization, lemmatization with spaCy.

**`app/services/nlp/skill_matcher.py`**: `rapidfuzz`-based fuzzy matching of skill strings against `Skill.aliases` catalogue (resolves "JS" → "javascript").

---

### 4.10 Data Seeding Scripts

| Script | Purpose |
|--------|---------|
| `scripts/seed.py` (23 KB) | Full seeder: reads 4 JSON files → batch upserts into PostgreSQL |
| `scripts/seed_neon_db.py` | Neon-specific seeder using `DATABASE_URL` for cloud DB |
| `scripts/ingest_jobs.py` | Reads `indian-job-market-dataset-2025.xlsx` (100k+ rows) → pandas ETL → `raw_jobs` / `job_cache` |
| `scripts/init_db.sql` | `CREATE EXTENSION IF NOT EXISTS vector;` |

---

## 5. Frontend V2 — Deep Dive

### 5.1 Tech Stack

| Tool | Version | Role |
|------|---------|------|
| React | 19.2.4 | UI library |
| react-router-dom | 7.14.0 | Client-side routing |
| Vite | 8.0.4 | Build tool + dev server (port 5173) |
| Tailwind CSS | 3.4.19 | Utility-first CSS |
| @hello-pangea/dnd | 18.0.1 | Drag-and-drop (Kanban board) |
| postcss + autoprefixer | Latest | CSS processing |
| ESLint | 9.39.4 | Linting |

> **Styling note**: Most pages use Tailwind utilities heavily for content. Layout primitives (sidebar, fixed positions) use inline `style` objects. Both patterns coexist throughout the codebase.

---

### 5.2 Design System & Aesthetics

The v2 frontend uses a **Neobrutalism** design aesthetic.

**Colour Palette**:

| Token | Hex | Usage |
|-------|-----|-------|
| Dark Green | `#1A4D2E` | Primary buttons, active nav, accents |
| Lavender | `#D8B4FE` | AI-themed elements, secondary highlights |
| Yellow | `#FACC15` | Warning, "Learning" skill badges |
| Near Black | `#1a1c1c` | Text, borders |
| Off White | `#F9FAFB` | Page backgrounds |
| White | `#FFFFFF` | Cards, inputs |

**Shadow System** (consistent across all pages):

```js
const NEO     = { boxShadow: "4px 4px 0px 0px #000000" }  // Standard cards
const NEO_SM  = { boxShadow: "2px 2px 0px 0px #000000" }  // Buttons, small elements
const NEO_LAV = { boxShadow: "6px 6px 0px 0px #D8B4FE" }  // AI-themed elements
const NEO_GRN = { boxShadow: "6px 6px 0px 0px #1A4D2E" }  // Success/primary elements
```

**Typography**:

| Font | Usage |
|------|-------|
| `Syne` (Google Fonts) | Headings — bold, uppercase |
| `Space Grotesk` (Google Fonts) | Body, UI text |
| `Lexend` (Google Fonts) | Sidebar nav — high legibility at small sizes |
| `Inter` (Google Fonts) | Fallback |

**Borders**: Always `border-2 border-black` — thick black border is a core neobrutalism trait.

**Interactions**: Hover → `hover:translate-x-[2px] hover:translate-y-[2px]` creates a "pressed" 3D effect offsetting the shadow.

**Icon library**: Google Material Symbols Outlined, loaded via `<link>` in JSX.

---

### 5.3 Application Routing

All routes defined in `src/App.jsx`:

| Path | Layout | Component | Type |
|------|--------|-----------|------|
| `/` | PublicLayout | `JobForLanding` | Public marketing |
| `/opportunities` | PublicLayout | `BigOpportunities` | Public |
| `/insights` | **AppLayout** | `MarketInsights` | App (auth intended) |
| `/skill-gap` | PublicLayout | `SkillGapAnalysis` | Public |
| `/coach` | **AppLayout** | `CareerCoach` | App (auth intended) |
| `/job` | PublicLayout | `JobDetail` | Public |
| `/join` | None | `JoinCommunity` | Standalone |
| `/login` | None | `LoginPage` | Standalone |
| `/reset` | None | `ResetPassword` | Standalone |
| `/user` | **AppLayout** | `UserDashboard` | App |
| `/applied` | **AppLayout** | `JobForDashboard` | App |
| `/saved` | **AppLayout** | `SavedJobs` | App |
| `/ai` | **AppLayout** | `AIRecommendations` | App |
| `/discover` | **AppLayout** | `JobDiscovery` | App |
| `/profile` | **AppLayout** | `EditProfile` | App |
| `/settings` | **AppLayout** | `SettingsPage` | App |
| `/analyzer` | **AppLayout** | `ResumeAnalyzer` | App |
| `*` | PublicLayout | `NotFound` | Public |

> **⚠️ No auth guards exist.** Any route wrapped in `AppLayout` is accessible without login. Route protection must be added.

---

### 5.4 Layout Architecture

**`PublicLayout`**: `PublicNavbar` (top) + `{children}` + `PublicFooter` (bottom)

**`AppLayout`** (authenticated shell):

```
┌───────────────────────────────────────────┐
│        AppHeader (fixed, h=80px)          │
├────────────┬──────────────────────────────┤
│            │                              │
│ AppSidebar │       {children}             │
│ (fixed,    │  (paddingTop: 80px,          │
│  w=288px)  │   marginLeft: 288px)         │
│            │                              │
└────────────┴──────────────────────────────┘
```

**`AppSidebar`** details:
- Fixed left, top=80px (below header), background `#f9f9f9`, right border `4px solid #1a1c1c`
- User mini-card at top (avatar, name, role) — currently hardcoded as "Alex Chen / Senior Architect"
- 9 navigation items (see §5.6)
- Active state: `background #1A4D2E`, white text, inner right shadow with `#D8B4FE`
- Bottom widget: "AI Match Score: 94%" + "Profile 78% complete" (hardcoded)

---

### 5.5 All Pages — Detailed Breakdown

#### `JobForLanding.jsx` (`/`) — ~18 KB
Marketing homepage. Hero section, feature highlights, CTAs to `/login` and `/join`. Uses PublicLayout.

#### `LoginPage.jsx` (`/login`) — ~15 KB
Full-screen standalone auth page. Email/password form, forgot password link, social auth placeholders. Auth is currently hardcoded credentials (`test@gmail.com` / `123@Test`) per dev setup.

#### `ResetPassword.jsx` (`/reset`) — ~12 KB
Standalone token-based password reset form.

#### `UserDashboard.jsx` (`/user`) — ~19 KB
Summary view: profile completion progress, recent activity widget, quick stats (saved jobs, applications, AI match), recommended next actions.

#### `JobForDashboard.jsx` (`/applied`) — ~18 KB
**Kanban Board** for application tracking. Columns map to `kanban_column` values. Uses `@hello-pangea/dnd` for drag-and-drop between columns. Cards display `status_label`, `status_icon`, `time_label` with DB-driven color theming (`time_label_bg`, `time_label_color`).

#### `SavedJobs.jsx` (`/saved`) — ~16 KB
Unified saved jobs + tracking view. Tab toggle between "Saved Jobs" and "Tracking" (Applied). No collections sidebar, no bulk actions (deliberately simplified per design history). Clean card list.

#### `JobDiscovery.jsx` (`/discover`) — ~29 KB
Primary job search page: search bar + role/location/type/exp/salary/remote filters, job listing cards, pagination.

#### `AIRecommendations.jsx` (`/ai`) — ~33 KB
Personalized ML recommendation display. Shows match score %, per-factor breakdown (skills, content, experience, location, salary), "Why this matches" explainer, filter/sort controls.

#### `JobDetail.jsx` (`/job`) — ~31 KB
Full job detail: company header (logo, metadata), full description, requirements, skills with match indicators, Apply/Save/Share buttons, similar jobs section.

#### `CareerCoach.jsx` (`/coach`) — ~14 KB

Chat interface. **Critical note: currently bypasses the backend and calls Anthropic directly from the browser:**

```js
const res = await fetch("https://api.anthropic.com/v1/messages", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    model: "claude-sonnet-4-20250514",
    max_tokens: 1000,
    system: SYSTEM_PROMPT,
    messages: apiMessages,
  }),
});
```

> **⚠️ Security Issue**: API key exposed in browser bundle. Must route through backend before production.

Layout:
- Left panel: Chat history list, saved tips panel
- Main: Message bubbles (welcome card, user right-aligned, assistant left-aligned)
- Special rendering: detected interview questions wrapped in quotes get a distinct highlighted block
- Input: Auto-resize textarea, quick prompts (`[Review Resume]`, `[Practice Interview]`, `[Cover Letter]`, `[Explain Salary Gap]`), Send button

#### `MarketInsights.jsx` (`/insights`) — ~17 KB

Data visualization dashboard. **All data currently hardcoded** (not fetched from backend).

Sections:
1. **Filters**: Role Type + Location selects (state-wired but not yet API-connected)
2. **Salary Insights** card: min/median/max range bar, percentile rank, "Your Estimate" pin
3. **Market Overview** card (purple bg): growth %, new postings, avg time-to-hire
4. **Top In-Demand Skills**: bars with `YOU HAVE / LEARNING / MISSING` badges
5. **Salary Trends**: 3-year SVG line chart (two paths: Market + Target)
6. **Top Hiring Companies**: icon + name + role count list
7. **Experience Level Distribution**: bar chart
8. **Geographic Distribution**: country % grid + decorative SVG world map
9. **CTA Banner**: "Update Profile" + "Find Matches" buttons

#### `ResumeAnalyzer.jsx` (`/analyzer`) — ~21 KB
PDF upload dropzone → calls `POST /api/v1/profile/me/resume` → displays parsed scores (overall, ATS), strengths, improvements, suggestions.

#### `SkillGapAnalysis.jsx` (`/skill-gap`) — ~10 KB
Public-facing skill gap visualizer for a target role. May connect to `/insights/skill-gap` or show a static demo.

#### `BigOpportunities.jsx` (`/opportunities`) — ~11 KB
Public page showcasing high-value jobs and growth-stage company opportunities.

#### `EditProfile.jsx` (`/profile`) — ~35 KB (largest page)
Full profile editor:
- Personal info, headline, summary
- Work experience CRUD (add/edit/delete)
- Education CRUD
- Certification CRUD
- Skills management (proficiency, primary flag)
- Salary & job preferences (remote pref, salary range, notice period)
- Social links (LinkedIn, GitHub, portfolio)
- Profile completion progress bar

All CRUD calls wire to the `/profile/*` endpoints.

#### `SettingsPage.jsx` (`/settings`) — ~34 KB
Account details (email, password change), notification preferences, privacy settings, job alert management, danger zone (account deletion).

#### `JoinCommunity.jsx` (`/join`) — ~20 KB
Community/waitlist signup page. Standalone (no layout).

#### `NotFound.jsx` (`*`) — ~7 KB
Custom 404 inside PublicLayout.

---

### 5.6 Shared Components

| Component | Purpose |
|-----------|---------|
| `AppLayout` | Authenticated page shell (AppHeader + AppSidebar + content area) |
| `AppHeader` | Fixed top bar — logo, search, notification bell, avatar |
| `AppSidebar` | Fixed left nav — 9 items: Dashboard, Discover, Insights, Big Opps, Saved Jobs, AI Coach, Resume Analyzer, Profile, Settings |
| `PublicLayout` | Public page shell — PublicNavbar + PublicFooter |
| `PublicNavbar` | Marketing nav with logo, links, and CTA buttons |
| `PublicFooter` | Footer with links and credits |
| `Navbar` | Simpler alternate navbar (may be legacy) |
| `Footer` | Simpler alternate footer |
| `NeoButton` | Reusable neobrutalism button with shadow + hover translate |
| `SectionTitle` | Styled heading with subtitle |

---

## 6. Data Files

Located in `jobfor/data/`:

| File | Size | Content |
|------|------|---------|
| `companies.json` | 13 KB | Company objects: name, industry, size, headquarters, culture ratings |
| `job_cache.json` | 64 KB | Job listings matching `JobCache` schema |
| `skills.json` | 16 KB | Skills: name, category, aliases, demand_score, is_trending |
| `market_insight_snapshots.json` | 28 KB | Pre-computed insight records for seeding `MarketInsightCache` |

Source: derived from `indian-job-market-dataset-2025.xlsx` (31 MB Excel) via `scripts/ingest_jobs.py`.

---

## 7. Key Architectural Decisions

### Dual Database Sessions (Sync + Async)
- **Sync (`psycopg2`)**: Alembic + startup health check only (Alembic cannot be async).
- **Async (`asyncpg`)**: All FastAPI route handlers — avoids blocking the event loop.

### HNSW Indexes on Vector Columns
Both `Profile.embedding` and `JobCache.embedding` have HNSW indexes (m=16, ef_construction=64) for fast approximate nearest-neighbor cosine similarity. Enables semantic matching without full table scans.

### JSONB for Multi-Value Preferences
`preferred_locations`, `job_type_preference`, `career_interests`, `skills_required` use JSONB + GIN indexes instead of separate junction tables. Enables efficient containment queries (`@>`) without schema changes.

### MarketInsightCache as DB-Backed TTL Cache
Analytics results are stored in a PostgreSQL table (not Redis) with `expires_at`. This makes the cache persistent across restarts, queryable via SQL, and avoids Redis dependency for non-critical analytics.

### Kanban Metadata Stored in `JobApplication`
`kanban_column`, `kanban_position`, `status_label`, `status_icon`, `time_label`, `time_label_bg`, `time_label_color` are stored on the application row. The database is the source of truth for drag-and-drop ordering — frontend just reads and writes positions.

### Job Snapshots in ATS Tables
`SavedJob.job_data` and `JobApplication.job_data` store a JSONB snapshot at save/apply time. Cards remain intact even if the `JobCache` row is later deactivated or modified.

---

## 8. Known Patterns & Conventions

### Backend Conventions
1. **All routes are async** → always `AsyncSession` via `Depends(get_async_db)`
2. **`selectinload` always explicit** — never call relationships without pre-loading in async context
3. **`model_dump(exclude_unset=True)`** for PATCH-style partial updates
4. **`await db.flush()` before using auto-generated PKs** when creating related objects in the same transaction
5. **`expire_on_commit=False`** — permits attribute access after commit without triggering lazy loads
6. **All errors raised as `HTTPException`** from the service layer — global handler formats them consistently
7. **Services are stateless static methods** (RecommendationService, InsightsService, JobService) except AuthService and ProfileService which are instantiated per-request with `self.db`

### Frontend Conventions
1. **Neobrutalism shadow constants** defined at module level in every page file
2. **Inline `style` for layout/fixed elements**, Tailwind classes for content styling
3. **Google Fonts loaded inline in JSX** — `<link>` inside component return (not ideal for performance)
4. **Hardcoded mock data** in many pages — intentional placeholder until API wiring is complete
5. **No global state** — no Redux, Zustand, or Context. Each page owns local state via `useState`
6. **No auth guards** — `AppLayout` routes have no redirect-if-unauthenticated logic yet

---

## 9. Current Limitations & TODOs

### 🔴 High Priority

- [ ] **CareerCoach → backend**: Wire `CareerCoach.jsx` to `POST /api/v1/ai-coach/chat` SSE endpoint. Currently calls Anthropic directly from the browser — API key exposed.
- [ ] **Route guards**: Add `PrivateRoute` or auth check in `AppLayout` to redirect unauthenticated users to `/login`.
- [ ] **API integration**: Most v2 pages use hardcoded data. These need live API calls: `MarketInsights`, `UserDashboard`, `AIRecommendations`, `SavedJobs`, `JobForDashboard`.
- [ ] **AuthContext in v2**: No token storage, no login/logout helpers, no user context exists. Must be built.

### 🟡 Medium Priority

- [ ] **Token refresh flow**: No frontend logic to refresh the access token when it expires.
- [ ] **Real email sending**: `request_password_reset` logs reset URL but does not send email via `aiosmtplib`.
- [ ] **OAuth implementation**: Google and GitHub OAuth endpoints are stubs.
- [ ] **S3 file storage**: Resume uploads save to local `uploads/` directory. Needs S3/MinIO integration for production.
- [ ] **Profile completion background task**: Currently computed only on resume upload. Should be a Celery periodic task.
- [ ] **Sidebar user data**: `DEFAULT_USER` ("Alex Chen") hardcoded. Needs authenticated user context.
- [ ] **MarketInsights filters**: Role/Location dropdowns update local state but never trigger API calls.

### 🟢 Low Priority

- [ ] **Alembic migration files**: Formal migration files should be generated for all models.
- [ ] **Blockchain verification fields**: `verification_hash` and `is_verified_on_chain` on Education/Certification are stubs — no integration.
- [ ] **Celery production deployment**: No supervisord/K8s worker config. `sync_external_jobs` requires valid Adzuna/RapidAPI keys.
- [ ] **Full-text search optimization**: GIN full-text index exists on `job_cache` but `search_jobs` may use `ILIKE` — verify and switch to `ts_query` for large datasets.
- [ ] **Skill demand weekly update**: `Skill.demand_score` should be refreshed weekly via Celery.

---

*End of Documentation*
