import logging
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any

import asyncio
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.async_database import async_db_session
from app.models.models import JobCache, JobAlert, Notification, AlertFrequency

logger = logging.getLogger(__name__)


async def sync_external_jobs() -> None:
    """
    Asynchronous network loop pulling data into JobCache natively leveraging 
    HTTPX bindings against Adzuna and RapidAPI JSearch targets.
    """
    import httpx
    import asyncio
    from app.core.config import settings
    
    async with async_db_session() as db:
        try:
            logger.info("Executing periodic external API job ingestion mapping...")
            
            # Setup network connections safely dropping connections if timeout hit
            async with httpx.AsyncClient(timeout=15.0) as client:
                
                # Fetch targets concurrently
                adz_task = asyncio.create_task(
                    client.get(
                        "https://api.adzuna.com/v1/api/jobs/in/search/1", 
                        params={
                            "app_id": settings.ADZUNA_APP_ID, 
                            "app_key": settings.ADZUNA_APP_KEY, 
                            "what": "software engineer",
                            "results_per_page": 20
                        }
                    )
                )
                
                jsc_task = asyncio.create_task(
                    client.get(
                        "https://jsearch.p.rapidapi.com/search",
                        headers={
                            "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
                            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
                        },
                        params={
                            "query": "software engineer in India",
                            "page": "1",
                            "num_pages": "1"
                        }
                    )
                )
                
                logger.info("Awaiting Remote API Resolution bounds...")
                responses = await asyncio.gather(adz_task, jsc_task, return_exceptions=True)
                
            jobs_to_insert = []
            
            # 1. Digest Adzuna Payload
            adz_res = responses[0]
            if isinstance(adz_res, httpx.Response) and adz_res.status_code == 200:
                body = adz_res.json()
                results = body.get("results", [])
                for element in results:
                    jobs_to_insert.append(JobCache(
                        external_id=str(element.get("id", "")),
                        title=element.get("title", "Unknown Role"),
                        company=element.get("company", {}).get("display_name", "Unknown"),
                        location=element.get("location", {}).get("display_name", "Remote"),
                        description=element.get("description", ""),
                        salary_min=element.get("salary_min"),
                        salary_max=element.get("salary_max"),
                        currency="INR",
                        source="Adzuna"
                    ))
            elif isinstance(adz_res, Exception):
                logger.warning(f"Adzuna Timeout/Exception: {str(adz_res)}")
                
            # 2. Digest JSearch Payload
            jsc_res = responses[1]
            if isinstance(jsc_res, httpx.Response) and jsc_res.status_code == 200:
                body = jsc_res.json()
                results = body.get("data", [])
                for element in results:
                    jobs_to_insert.append(JobCache(
                        external_id=element.get("job_id", ""),
                        title=element.get("job_title", "Unknown Role"),
                        company=element.get("employer_name", "Unknown"),
                        location=f"{element.get('job_city', '')}, {element.get('job_country', '')}",
                        description=element.get("job_description", ""),
                        salary_min=element.get("job_min_salary"),
                        salary_max=element.get("job_max_salary"),
                        currency="USD" if element.get("job_salary_currency") == "USD" else "INR",
                        source="JSearch",
                        remote=element.get("job_is_remote", False)
                    ))
            elif isinstance(jsc_res, Exception):
                logger.warning(f"JSearch Timeout/Exception: {str(jsc_res)}")

            # Execute Bulk Upsert structurally bypassing errors safely
            if jobs_to_insert:
                for job in jobs_to_insert:
                    # Ignore existing keys gracefully minimizing database locks
                    stmt = select(JobCache).where(JobCache.external_id == job.external_id)
                    cursor = await db.execute(stmt)
                    if not cursor.scalars().first():
                        db.add(job)
                        
                await db.commit()
                logger.info(f"External HTTP sync concluded mapping {len(jobs_to_insert)} raw remote rows.")
            
        except Exception as e:
            logger.error(f"Failing explicitly inside job sync executor: {str(e)}")


async def process_job_alerts() -> None:
    """
    Background executor tracking users' subscribed SQL Alerts dynamically, comparing them to recent JobCache insertions, and natively generating Notification elements securely.
    """
    async with async_db_session() as db:
        try:
            # 1. Scope alerts structurally natively joining User fields for Notifications dynamically
            stmt = select(JobAlert).where(JobAlert.is_active == True).options(selectinload(JobAlert.user))
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
                    
                    search_link = f"/jobs?query={alert.keywords[0] if alert.keywords else ''}"
                    
                    notif = Notification(
                        user_id=alert.user_id,
                        type="JOB_ALERT",
                        title=f"New hits for '{alert.alert_name}'",
                        message=f"We discovered {match_count} new opportunities bridging your isolated alert parameters.",
                        link=search_link
                    )
                    db.add(notif)
                    total_notifications += 1
                    
                    # 4. Trigger Async SMTP natively
                    from app.services.email_service import send_job_alert_email
                    if alert.user and alert.user.email:
                        await send_job_alert_email(
                            to_email=alert.user.email,
                            job_count=match_count,
                            alert_name=alert.alert_name,
                            link=search_link
                        )
            
            await db.commit()
            logger.info(f"Background Job Alerts successfully dispatched {total_notifications} notification mappings.")
        except Exception as e:
            logger.error(f"Alert executor halted securely avoiding cascade: {str(e)}")


from app.core.celery_app import celery_app

@celery_app.task(name="app.services.scheduler_service.sync_external_jobs_task")
def sync_external_jobs_task() -> None:
    """
    Synchronous celery task wrapping asynchronous sync explicitly safely targeting API endpoints continuously natively.
    """
    asyncio.run(sync_external_jobs())


@celery_app.task(name="app.services.scheduler_service.process_job_alerts_task")
def process_job_alerts_task() -> None:
    """
    Synchronous celery task validating alert bindings safely triggering explicit SMTP pipelines against matching Job indices mapping cleanly.
    """
    asyncio.run(process_job_alerts())
