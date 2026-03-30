import json
import statistics
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional

from fastapi import HTTPException
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from openai import AsyncOpenAI

from app.core.config import settings
from app.models.models import MarketInsightCache, JobCache, Profile, User
from app.schemas.insights import SkillDemand

# Globally inject instance specifically scoped through env keys
openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


class InsightsService:

    @staticmethod
    async def get_salary_insights(db: AsyncSession, role: str, location: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculates and aggressively caches salary boundaries across JobCache records securely without blocking.
        Dynamically falls back to standard integer sets when jobs lack numerical properties natively. 
        """
        # 1. Probe Cache Hit
        param_sig = {"role": role, "location": location}
        stmt_cache = (
            select(MarketInsightCache)
            .where(
                MarketInsightCache.insight_type == "salary_trend",
                MarketInsightCache.expires_at > datetime.now(timezone.utc)
            )
        )
        cursor_cache = await db.execute(stmt_cache)
        matches = [c for c in cursor_cache.scalars().all() if c.parameters == param_sig]
        if matches:
            return matches[0].data

        # 2. Recompute directly hitting the raw index dynamically
        stmt_jobs = select(JobCache).where(
            and_(
                JobCache.is_active == True,
                JobCache.title.ilike(f"%{role}%")
            )
        )
        if location:
            stmt_jobs = stmt_jobs.where(JobCache.location.ilike(f"%{location}%"))

        cursor_jobs = await db.execute(stmt_jobs)
        jobs = cursor_jobs.scalars().all()

        salaries = []
        for j in jobs:
            if j.salary_min and j.salary_max:
                salaries.extend([j.salary_min, j.salary_max])
            elif j.salary_min:
                salaries.append(j.salary_min)
            elif j.salary_max:
                salaries.append(j.salary_max)

        if not salaries:
            # Fallback zeroed architecture if completely empty bounds map natively
            result_data = {"role": role, "location": location, "min": 0, "median": 0, "max": 0, "sampleSize": 0}
            return result_data

        # Math securely processed locally without locking postgres PERCENTILE loops
        salaries.sort()
        res_min = int(salaries[0])
        res_max = int(salaries[-1])
        res_median = int(statistics.median(salaries))
        sample_size = len(jobs)

        result_data = {
            "role": role,
            "location": location,
            "min": res_min,
            "median": res_median,
            "max": res_max,
            "sampleSize": sample_size
        }

        # 3. Cache Write (24 hrs TTL)
        cache_entry = MarketInsightCache(
            insight_type="salary_trend",
            parameters=param_sig,
            data=result_data,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=24)
        )
        db.add(cache_entry)
        await db.commit()
        
        return result_data

    @staticmethod
    async def get_skill_demand(db: AsyncSession, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Global map aggregating structural list arrays from all JSONB tags natively into proportional percentages.
        """
        param_sig = {"limit": limit}
        stmt_cache = (
            select(MarketInsightCache)
            .where(
                MarketInsightCache.insight_type == "skill_demand",
                MarketInsightCache.expires_at > datetime.now(timezone.utc)
            )
        )
        cursor_cache = await db.execute(stmt_cache)
        matches = [c for c in cursor_cache.scalars().all() if c.parameters == param_sig]
        if matches:
            return matches[0].data.get("demands", [])

        # Fetch actively listed structural tags locally
        stmt_jobs = select(JobCache.skills_required).where(
            and_(JobCache.is_active == True, JobCache.skills_required != None)
        )
        cursor = await db.execute(stmt_jobs)
        skill_lists = cursor.scalars().all()

        total_jobs = len(skill_lists)
        if total_jobs == 0:
            return []

        # Count frequencies
        freq_map = {}
        for s_list in skill_lists:
            # unique them per job recursively
            for skill in set(str(s).lower().strip() for s in s_list):
                freq_map[skill] = freq_map.get(skill, 0) + 1

        # Transform and sort map descending
        results = []
        sorted_skills = sorted(freq_map.items(), key=lambda item: item[1], reverse=True)

        for skill, count in sorted_skills[:limit]:
            results.append({
                "skill": skill,
                "demandPercentage": int((count / total_jobs) * 100)
            })

        # Cache Output structure
        cache_entry = MarketInsightCache(
            insight_type="skill_demand",
            parameters=param_sig,
            data={"demands": results},
            expires_at=datetime.now(timezone.utc) + timedelta(hours=24)
        )
        db.add(cache_entry)
        await db.commit()

        return results

    @staticmethod
    async def analyze_skill_gap(db: AsyncSession, user_id: int, target_role: str) -> Dict[str, Any]:
        """
        Highly targeted heuristic analysis extracting profile limits explicitly against targeted industry demands.
        Invokes AsyncOpenAI cleanly producing isolated arrays outlining gap milestones immediately.
        """
        # 1. Access user state safely
        prof_stmt = (
            select(Profile)
            .where(Profile.user_id == user_id)
            .options(selectinload(Profile.user).selectinload(User.skills))
        )
        p_cursor = await db.execute(prof_stmt)
        profile = p_cursor.scalars().first()

        if not profile:
            raise HTTPException(status_code=404, detail="User profile required.")

        user_skills = set(str(s.skill.name).lower().strip() for s in profile.user.skills) if profile.user.skills else set()

        # 2. Extract market definition (Top 15 skills for targeted role natively)
        j_stmt = select(JobCache.skills_required).where(
            and_(
                JobCache.is_active == True,
                JobCache.title.ilike(f"%{target_role}%"),
                JobCache.skills_required != None
            )
        )
        j_cursor = await db.execute(j_stmt)
        job_skill_arrays = j_cursor.scalars().all()
        
        job_count = len(job_skill_arrays)
        if job_count == 0:
            # Blank out successfully avoiding zero-division
            return {
                "targetRole": target_role,
                "readinessScore": 100.0 if user_skills else 0.0,
                "strongSkills": list(user_skills),
                "skillsToImprove": [],
                "missingCritical": [],
                "learningPath": []
            }

        market_map = {}
        for j_skills in job_skill_arrays:
            for sk in set(str(s).lower().strip() for s in j_skills):
                market_map[sk] = market_map.get(sk, 0) + 1

        sorted_market = sorted(market_map.items(), key=lambda x: x[1], reverse=True)[:15]

        # 3. Matrix sorting routine separating structural matches natively
        strong_lists = []
        improve_lists = []
        critical_lists = []
        points = 0.0
        max_points = 0.0

        for skill, count in sorted_market:
            demand_pct = int((count / job_count) * 100)
            max_points += demand_pct

            if skill in user_skills:
                strong_lists.append(skill)
                points += demand_pct
            else:
                if demand_pct >= 30:
                    critical_lists.append(SkillDemand(skill=skill.capitalize(), demandPercentage=demand_pct).model_dump())
                else:
                    improve_lists.append(skill.capitalize())

        readiness = round((points / max_points) * 100, 1) if max_points > 0 else 0.0

        # 4. Asynchronous GPT Execution
        missing_names = [c["skill"] for c in critical_lists] + improve_lists[:3]
        learning_path = []

        if missing_names:
            prompt = f"""You are an executive career architect.
            The user wants to become a "{target_role}" but strictly lacks these critical skills: {", ".join(missing_names)}.
            Generate a targeted, accelerated week-by-week learning roadmap strictly returning a JSON object with a single 'path' key containing a list of dictionaries with exactly 3 keys: 'week' (integer), 'title' (string), and 'resources' (list of exact string URLs or concepts).
            Keep it strictly under 4 weeks total.
            """
            
            try:
                response = await openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    response_format={"type": "json_object"},
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                json_payload = json.loads(response.choices[0].message.content)
                learning_path = json_payload.get("path", [])
            except Exception:
                # Provide empty mapping organically preventing system crashes over upstream errors
                pass

        return {
            "targetRole": target_role,
            "readinessScore": readiness,
            "strongSkills": [s.capitalize() for s in strong_lists],
            "skillsToImprove": improve_lists,
            "missingCritical": critical_lists,
            "learningPath": learning_path
        }
