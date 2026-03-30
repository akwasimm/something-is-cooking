from fastapi import HTTPException
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import JobCache
from app.schemas.job import JobSearchParams, PaginatedJobResponse


class JobService:
    @staticmethod
    async def search_jobs(db: AsyncSession, params: JobSearchParams) -> dict:
        stmt = select(JobCache).where(JobCache.is_active == True)

        if params.query:
            search_str = f"%{params.query}%"
            stmt = stmt.where(
                or_(
                    JobCache.title.ilike(search_str),
                    JobCache.company.ilike(search_str),
                )
            )

        if params.location:
            stmt = stmt.where(JobCache.location.ilike(f"%{params.location}%"))

        if params.remote is True:
            stmt = stmt.where(JobCache.is_remote == True)

        if params.job_type:
            stmt = stmt.where(JobCache.job_type.in_(params.job_type))

        if params.experience_level:
            stmt = stmt.where(JobCache.experience_level.in_(params.experience_level))

        if params.salary_min is not None:
            stmt = stmt.where(JobCache.salary_max >= params.salary_min)

        # Count total matching rows
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_cursor = await db.execute(count_stmt)
        total = total_cursor.scalar_one()

        # Apply ordering, pagination
        stmt = stmt.order_by(JobCache.posted_at.desc().nulls_last())
        offset_val = (params.page - 1) * params.limit
        stmt = stmt.offset(offset_val).limit(params.limit)

        cursor = await db.execute(stmt)
        jobs = cursor.scalars().all()

        return {
            "data": list(jobs),
            "total": total,
            "page": params.page,
            "limit": params.limit
        }

    @staticmethod
    async def get_job_by_id(db: AsyncSession, job_id: int) -> JobCache:
        job = await db.get(JobCache, job_id)
        if not job or not job.is_active:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
