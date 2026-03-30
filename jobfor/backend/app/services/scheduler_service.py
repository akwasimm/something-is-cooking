import logging
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.async_database import async_db_session
from app.models.models import JobCache, JobAlert, Notification, AlertFrequency

logger = logging.getLogger(__name__)


async def sync_external_jobs() -> None:
    """
    Simulated external network sync pulling data into JobCache.
    (Replace the internal contents cleanly with httpx requests to Adzuna or JSearch)
    """
    async with async_db_session() as db:
        try:
            logger.info("Executing periodic external API job ingestion mapping...")
            # Example API fetch placeholder logic:
            # results = await JobApiService.fetch_adzuna(limit=50)
            # for r in results:
            #     db.add(JobCache(**r))
            # await db.commit()
            logger.info("External sync successfully passed without crashing.")
        except Exception as e:
            logger.error(f"Failing explicitly inside job sync executor: {str(e)}")


async def process_job_alerts() -> None:
    """
    Background executor tracking users' subscribed SQL Alerts dynamically, comparing them to recent JobCache insertions, and natively generating Notification elements securely.
    """
    async with async_db_session() as db:
        try:
            # 1. Scope alerts structurally
            stmt = select(JobAlert).where(JobAlert.is_active == True)
            cursor = await db.execute(stmt)
            active_alerts = cursor.scalars().all()
            
            total_notifications = 0

            for alert in active_alerts:
                # Resolve mathematical loop times dynamically mapped
                loop_hrs = 24
                if alert.frequency == AlertFrequency.instant:
                    loop_hrs = 1
                elif alert.frequency == AlertFrequency.weekly:
                    loop_hrs = 168
                    
                lookback_window = alert.last_sent or (datetime.now(timezone.utc) - timedelta(hours=loop_hrs))

                # 2. Build Job search bounds natively matching the query limits exactly
                j_stmt = select(JobCache).where(
                    and_(
                        JobCache.is_active == True,
                        JobCache.created_at >= lookback_window
                    )
                )

                if alert.keywords and len(alert.keywords) > 0:
                    query = alert.keywords[0]
                    j_stmt = j_stmt.where(JobCache.title.ilike(f"%{query}%"))

                if alert.location:
                    j_stmt = j_stmt.where(JobCache.location.ilike(f"%{alert.location}%"))
                
                if alert.salary_min:
                    j_stmt = j_stmt.where(JobCache.salary_max >= alert.salary_min)
                
                j_cursor = await db.execute(j_stmt)
                matches = j_cursor.scalars().all()
                match_count = len(matches)

                # 3. Create active mapping rows triggering user UI dynamically
                if match_count > 0:
                    alert.last_sent = datetime.now(timezone.utc)
                    
                    notif = Notification(
                        user_id=alert.user_id,
                        type="JOB_ALERT",
                        title=f"New hits for '{alert.alert_name}'",
                        message=f"We discovered {match_count} new opportunities bridging your isolated alert parameters.",
                        link=f"/jobs?query={alert.keywords[0] if alert.keywords else ''}"
                    )
                    db.add(notif)
                    total_notifications += 1
            
            await db.commit()
            logger.info(f"Background Job Alerts successfully dispatched {total_notifications} notification mappings.")
        except Exception as e:
            logger.error(f"Alert executor halted securely avoiding cascade: {str(e)}")


def start_scheduler() -> None:
    """
    Initialize background AsyncIOScheduler linking specific functional logic inside looping interval triggers securely without exhausting FastAPI MainThread dependencies.
    """
    scheduler = AsyncIOScheduler(timezone="UTC")
    
    # Trigger job sync hourly dynamically protecting your caches
    scheduler.add_job(sync_external_jobs, 'interval', hours=1, id="sync_jobs")
    
    # Resolve alerts evaluating changes twice-a-day iteratively
    scheduler.add_job(process_job_alerts, 'interval', hours=12, id="trigger_alerts")
    
    scheduler.start()
    logger.info("AsyncIOScheduler operational and tracking jobs in background thread.")
