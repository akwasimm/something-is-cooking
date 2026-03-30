from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Notification, JobAlert, AlertFrequency
from app.schemas.notification import JobAlertCreate


class NotificationService:
    
    @staticmethod
    async def get_notifications(db: AsyncSession, user_id: int, unread_only: bool = False) -> List[Notification]:
        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
        )
        if unread_only:
            stmt = stmt.where(Notification.is_read == False)
            
        cursor = await db.execute(stmt)
        return list(cursor.scalars().all())

    @staticmethod
    async def mark_as_read(db: AsyncSession, user_id: int, notification_id: int) -> Notification:
        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id, Notification.id == notification_id)
        )
        cursor = await db.execute(stmt)
        notification = cursor.scalars().first()
        
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
            
        notification.is_read = True
        await db.commit()
        await db.refresh(notification)
        return notification

    @staticmethod
    async def mark_all_as_read(db: AsyncSession, user_id: int) -> int:
        stmt = (
            update(Notification)
            .where(Notification.user_id == user_id, Notification.is_read == False)
            .values(is_read=True)
            .execution_options(synchronize_session=False)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount

    @staticmethod
    async def delete_notification(db: AsyncSession, user_id: int, notification_id: int) -> None:
        stmt = (
            delete(Notification)
            .where(Notification.user_id == user_id, Notification.id == notification_id)
        )
        result = await db.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Notification not found")
            
        await db.commit()

    @staticmethod
    async def create_job_alert(db: AsyncSession, user_id: int, data: JobAlertCreate) -> JobAlert:
        # Convert remoteOnly bool logic cleanly into standardized JobTypes arrays if necessary
        job_types = data.jobTypes or []
        if data.remoteOnly and "Remote" not in job_types:
            job_types.append("Remote")

        try:
            enum_frequency = AlertFrequency[data.frequency.value]
        except KeyError:
            enum_frequency = AlertFrequency.daily
            
        new_alert = JobAlert(
            user_id=user_id,
            alert_name=data.name,
            keywords=[data.query], # Store the direct string query explicitly tracking matches
            location=data.location,
            job_type=job_types,
            salary_min=data.salaryMin,
            frequency=enum_frequency,
            is_active=True
        )
        db.add(new_alert)
        await db.commit()
        await db.refresh(new_alert)
        return new_alert

    @staticmethod
    async def get_job_alerts(db: AsyncSession, user_id: int) -> List[JobAlert]:
        stmt = select(JobAlert).where(JobAlert.user_id == user_id).order_by(JobAlert.created_at.desc())
        cursor = await db.execute(stmt)
        return list(cursor.scalars().all())
