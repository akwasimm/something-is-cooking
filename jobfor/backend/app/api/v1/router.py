from fastapi import APIRouter
from app.api.v1.endpoints import health, jobs, applications, ai_coach, insights, notifications

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(applications.router, tags=["ATS"])
api_router.include_router(ai_coach.router, tags=["AI Coach"])
api_router.include_router(insights.router, tags=["Analytics & Insights"])
api_router.include_router(notifications.router, tags=["Notifications & Alerts"])
