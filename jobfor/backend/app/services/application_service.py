from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from fastapi import HTTPException
from sqlalchemy import select, and_, func, null
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.models import SavedJob, JobApplication, ApplicationStatus
from app.schemas.application import SaveJobCreate, JobApplicationCreate, ApplicationStatusUpdate


class ApplicationService:

    @staticmethod
    async def save_job(db: AsyncSession, user_id: int, data: SaveJobCreate) -> SavedJob:
        # Resolve numeric IDs versus external strings safely
        internal_job_id = None
        external_id = None
        if data.job_id.isdigit():
            internal_job_id = int(data.job_id)
        else:
            external_id = data.job_id
            
        # Prevent completely duplicate save interactions
        collision_stmt = select(SavedJob).where(SavedJob.user_id == user_id)
        if internal_job_id:
            collision_stmt = collision_stmt.where(SavedJob.job_id == internal_job_id)
        else:
            collision_stmt = collision_stmt.where(SavedJob.external_job_id == external_id)
            
        cursor = await db.execute(collision_stmt)
        if cursor.scalars().first():
            raise HTTPException(status_code=400, detail="Job already saved.")

        # Aggregate folder into tags conceptually
        tags = data.tags or []
        if data.folder != "default":
            tags.append(data.folder)

        saved = SavedJob(
            user_id=user_id,
            job_id=internal_job_id,
            external_job_id=external_id,
            job_data=data.job_data,
            notes=data.notes,
            tags=tags
        )
        
        db.add(saved)
        await db.commit()
        await db.refresh(saved)
        return saved

    @staticmethod
    async def get_saved_jobs(db: AsyncSession, user_id: int, folder: Optional[str] = None) -> List[SavedJob]:
        stmt = select(SavedJob).where(SavedJob.user_id == user_id).order_by(SavedJob.created_at.desc())
        
        if folder and folder != "default":
            # Native PostgreSQL JSONB containment testing for the string
            stmt = stmt.where(SavedJob.tags.contains([folder]))
            
        cursor = await db.execute(stmt)
        return list(cursor.scalars().all())

    @staticmethod
    async def unsave_job(db: AsyncSession, user_id: int, saved_job_id: int):
        saved = await db.get(SavedJob, saved_job_id)
        if not saved or saved.user_id != user_id:
            raise HTTPException(status_code=404, detail="Saved job not found.")
            
        await db.delete(saved)
        await db.commit()
    
    @staticmethod
    async def apply_to_job(db: AsyncSession, user_id: int, data: JobApplicationCreate) -> JobApplication:
        # Resolve ID structures
        internal_job_id = None
        external_id = None
        if data.job_id.isdigit():
            internal_job_id = int(data.job_id)
        else:
            external_id = data.job_id

        # Unique Constraint validation against identical applications
        collision_stmt = select(JobApplication).where(JobApplication.user_id == user_id)
        if internal_job_id:
            collision_stmt = collision_stmt.where(JobApplication.job_id == internal_job_id)
        else:
            collision_stmt = collision_stmt.where(JobApplication.external_job_id == external_id)
            
        cursor = await db.execute(collision_stmt)
        if cursor.scalars().first():
            raise HTTPException(status_code=400, detail="Application already exists for this job.")

        # Create record tracking Resume/Cover Letter cleanly inside metadata properties
        app = JobApplication(
            user_id=user_id,
            job_id=internal_job_id,
            external_job_id=external_id,
            job_data=data.job_data,
            resume_used=data.resume_used,
            cover_letter=data.cover_letter,
            notes=data.notes,
            status=ApplicationStatus.applied
        )
        
        db.add(app)
        
        # Optionally cleanup SavedJobs pipeline if applicable
        cleanup_stmt = select(SavedJob).where(SavedJob.user_id == user_id)
        if internal_job_id:
            cleanup_stmt = cleanup_stmt.where(SavedJob.job_id == internal_job_id)
        else:
            cleanup_stmt = cleanup_stmt.where(SavedJob.external_job_id == external_id)
            
        saved_cursor = await db.execute(cleanup_stmt)
        saved_match = saved_cursor.scalars().first()
        if saved_match:
            await db.delete(saved_match)

        await db.commit()
        await db.refresh(app)
        return app

    @staticmethod
    async def get_applications(db: AsyncSession, user_id: int, status: Optional[ApplicationStatus] = None) -> List[JobApplication]:
        stmt = select(JobApplication).where(JobApplication.user_id == user_id)
        if status:
            stmt = stmt.where(JobApplication.status == status)
        
        stmt = stmt.order_by(JobApplication.applied_at.desc())
        cursor = await db.execute(stmt)
        return list(cursor.scalars().all())

    @staticmethod
    async def update_application_status(
        db: AsyncSession, user_id: int, app_id: int, data: ApplicationStatusUpdate
    ) -> JobApplication:
        app = await db.get(JobApplication, app_id)
        if not app or app.user_id != user_id:
            raise HTTPException(status_code=404, detail="Application not found.")

        # Adjust the core status properties
        if app.status != data.status:
            app.status = data.status
            app.status_updated_at = datetime.now(timezone.utc)
            
        if data.notes:
            app.notes = f"{app.notes}\n{data.notes}" if app.notes else data.notes
            
        if data.follow_up_date:
            # We strictly expect a datetime but schema drops Date property map elegantly
            app.follow_up_date = data.follow_up_date.date()

        if data.interview_date:
            dates = app.interview_dates or []
            # We enforce appending timestamps explicitly into JSONB without overriding existing data
            dates.append(data.interview_date.isoformat())
            # Reassign so ORM detects mutation
            app.interview_dates = dates
            
        await db.commit()
        await db.refresh(app)
        return app

    @staticmethod
    async def get_application_stats(db: AsyncSession, user_id: int) -> Dict[str, Any]:
        stmt = (
            select(JobApplication.status, func.count(JobApplication.id))
            .where(JobApplication.user_id == user_id)
            .group_by(JobApplication.status)
        )
        cursor = await db.execute(stmt)
        tallies = cursor.all()
        
        breakdown = {status.value: count for status, count in tallies}
        total = sum(breakdown.values())
        
        return {
            "total": total,
            "breakdown": breakdown
        }
