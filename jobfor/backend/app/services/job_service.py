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

    @staticmethod
    async def get_trending_jobs(db: AsyncSession, limit: int = 10) -> list[JobCache]:
        """
        Retrieves the newest array of listings explicitly targeting market volatility natively.
        """
        stmt = (
            select(JobCache)
            .where(JobCache.is_active == True)
            .order_by(JobCache.posted_at.desc().nulls_last())
            .limit(limit)
        )
        cursor = await db.execute(stmt)
        return list(cursor.scalars().all())

    @staticmethod
    async def get_similar_jobs(db: AsyncSession, job_id: int, limit: int = 10) -> list[JobCache]:
        """
        Performs JSONB structural overlap querying locally returning natively weighted heuristic arrays.
        """
        # 1. Fetch Target Job
        target_job = await JobService.get_job_by_id(db, job_id)
        if not target_job.skills_required:
            return []
            
        target_skills = set(str(s).lower().strip() for s in target_job.skills_required)
        if not target_skills:
            return []

        # 2. Query potential matches sharing structural boundaries natively
        stmt = (
            select(JobCache)
            .where(
                JobCache.is_active == True,
                JobCache.id != job_id,
                JobCache.skills_required != None
            )
        )
        cursor = await db.execute(stmt)
        candidates = cursor.scalars().all()
        
        # 3. Compute Jaccard Index Locally
        scored_candidates = []
        for candidate in candidates:
            if not candidate.skills_required:
                continue
                
            c_skills = set(str(s).lower().strip() for s in candidate.skills_required)
            intersection = len(target_skills.intersection(c_skills))
            union = len(target_skills.union(c_skills))
            
            if union == 0:
                continue
                
            jaccard_score = intersection / union
            
            # Require at least some overlap natively mitigating blank scores
            if jaccard_score > 0:
                scored_candidates.append((jaccard_score, candidate))
                
        # 4. Sort Descending & apply limits statically
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        return [c[1] for c in scored_candidates[:limit]]
