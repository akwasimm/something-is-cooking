import logging
from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

logger = logging.getLogger(__name__)

celery_app = Celery(
    "jobfor_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.services.scheduler_service"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,
)

celery_app.conf.beat_schedule = {
    "sync-jobs-hourly": {
        "task": "app.services.scheduler_service.sync_external_jobs_task",
        "schedule": crontab(minute=0),
    },
    "process-alerts-twice-daily": {
        "task": "app.services.scheduler_service.process_job_alerts_task",
        "schedule": crontab(minute=0, hour="0,12"),
    },
}

logger.info("Celery scaled architecture injected mapping Redis brokers securely.")
