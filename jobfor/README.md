# JobFor 🚀

A job board application with a **React** frontend and a **Python (FastAPI)** backend.

## Project Structure

```
jobfor/
├── frontend/   # React + Vite
└── backend/    # Python FastAPI REST API
```

---

## Frontend (React + Vite)

### Tech Stack
- React 18
- Vite (dev server + bundler)

### Setup & Run

```bash
cd frontend
npm install        # already done during setup
npm run dev        # starts on http://localhost:5173
```

---

## Backend (Python FastAPI)

### Tech Stack
- FastAPI — REST framework
- SQLAlchemy 2 — ORM
- Alembic — database migrations
- Pydantic v2 — data validation
- Uvicorn — ASGI server
- SQLite (default) — swap for PostgreSQL via `.env`

### Setup & Run

```bash
cd backend
# Activate virtual environment
.\.venv\Scripts\activate      # Windows
source .venv/bin/activate     # macOS/Linux

# Copy env file and configure
cp .env.example .env

# Run migrations
alembic upgrade head

# Start dev server
uvicorn main:app --reload     # starts on http://localhost:8000
```

### API Docs
Once running, visit:
- **Swagger UI** → http://localhost:8000/docs
- **ReDoc** → http://localhost:8000/redoc

### Available Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET | `/api/v1/health` | Service health |
| GET | `/api/v1/jobs` | List jobs |
| GET | `/api/v1/jobs/{id}` | Get single job |
| POST | `/api/v1/jobs` | Create a job |
| DELETE | `/api/v1/jobs/{id}` | Delete a job |

---

## Environment Variables (backend)

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./jobfor.db` | Database connection string |
| `SECRET_KEY` | — | JWT signing key |
| `ALLOWED_ORIGINS` | `["http://localhost:5173"]` | CORS allowed origins |
