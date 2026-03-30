from typing import List, Dict, Any
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from app.models.models import JobCache, Profile, User, WorkExperience


class RecommendationService:
    @staticmethod
    def calculate_skill_match(user_skills: List[str], job_skills: List[str]) -> float:
        """
        Calculates Jaccard Similarity (Intersection over Union) for skills.
        """
        if not user_skills or not job_skills:
            return 0.0
            
        set_u = set([s.lower() for s in user_skills])
        set_j = set([s.lower() for s in job_skills])
        
        intersection = len(set_u.intersection(set_j))
        union = len(set_u.union(set_j))
        
        return float(intersection / union) if union > 0 else 0.0

    @staticmethod
    def calculate_content_match(user_text: str, job_texts: List[str]) -> List[float]:
        """
        Calculates TF-IDF Cosine Similarity for semantic matching between 
        the user's profile contents versus a list of job descriptions.
        """
        if not user_text or not job_texts:
            return [0.0] * len(job_texts)
            
        vectorizer = TfidfVectorizer(stop_words='english')
        # Combined corpus: index 0 is the user, indices 1..N are jobs
        corpus = [user_text] + job_texts
        
        try:
            tfidf_matrix = vectorizer.fit_transform(corpus)
            # cosine_similarity returns a matrix, we extract the row 0 (user) against jobs (columns 1..N)
            similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
            return similarities.tolist()
        except ValueError:
            # Vocabulary empty
            return [0.0] * len(job_texts)

    @staticmethod
    def calculate_experience_match(user_exp: float, job_exp_level: str) -> float:
        """
        A heuristic function mapping the numerical user experience (in years)
        against the categorical or non-categorical job's experience level.
        """
        if not job_exp_level:
            return 0.5  # Neutral if unrestricted
            
        level = job_exp_level.lower()
        if user_exp is None:
            return 0.0

        if "entry" in level or "junior" in level:
            if user_exp <= 2.0: return 1.0
            if user_exp <= 4.0: return 0.7
            return 0.3 # Overqualified
        elif "mid" in level:
            if 2.0 <= user_exp <= 5.0: return 1.0
            if user_exp > 5.0: return 0.8
            if user_exp < 2.0: return 0.4
        elif "senior" in level or "lead" in level:
            if user_exp >= 5.0: return 1.0
            if 3.0 <= user_exp < 5.0: return 0.6
            return 0.2
        elif "director" in level or "executive" in level:
            if user_exp >= 8.0: return 1.0
            if 5.0 <= user_exp < 8.0: return 0.5
            return 0.1

        # Fallback numeric inference if the level contains numbers, though rare for 'str' fields
        return 0.5
        
    @staticmethod
    def calculate_location_match(user_locations: List[str], remote_pref: str, job_location: str, is_remote: bool) -> float:
        if is_remote and remote_pref in ["remote", "any"]:
            return 1.0
            
        if not job_location or not user_locations:
            return 0.5
            
        for loc in user_locations:
            if loc.lower() in job_location.lower() or job_location.lower() in loc.lower():
                return 1.0
        return 0.0
        
    @staticmethod
    def calculate_salary_match(user_min: int, job_min: int, job_max: int) -> float:
        if not user_min:
            return 0.5
        if not job_max and not job_min:
            return 0.5
            
        effective_job_max = job_max or job_min
        if user_min <= effective_job_max:
            return 1.0
        
        gap = user_min - effective_job_max
        # Decay match sharply if job pays less than expected minimum
        if gap < user_min * 0.2: # within 20%
            return 0.8
        if gap < user_min * 0.4:
            return 0.4
        return 0.1

    @staticmethod
    async def get_recommendations(db: AsyncSession, user_id: int, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Hybrid Semantic Recommendation Orchestrator.
        Fetches DB dependencies, runs the analytical engine matrix, weights results, and returns top-K.
        """
        # 1. Fetch User Profile
        stmt_prof = (
            select(Profile)
            .where(Profile.user_id == user_id)
            .options(
                selectinload(Profile.user).selectinload(User.skills),
                selectinload(Profile.user).selectinload(User.work_experiences)
            )
        )
        cursor_prof = await db.execute(stmt_prof)
        profile = cursor_prof.scalars().first()

        if not profile:
            raise HTTPException(status_code=404, detail="User profile required for recommendations.")

        # 2. Extract profile vectors
        user_skills = [s.skill.name for s in profile.user.skills] if profile.user.skills else []
        
        # Build giant text clump for TF-IDF Semantic matching
        exp_texts = " ".join([f"{e.job_title} at {e.company_name}: {e.description or ''}" for e in profile.user.work_experiences])
        user_text = f"{profile.headline or ''} {profile.summary or ''} {exp_texts}".strip()
        
        user_exp = profile.experience_years or 0.0
        user_locs = profile.preferred_locations or [profile.location] if profile.location else []
        remote_pref = (profile.remote_preference.value if profile.remote_preference else "any")
        
        # 3. Fetch active Jobs
        cursor_jobs = await db.execute(select(JobCache).where(JobCache.is_active == True))
        jobs = cursor_jobs.scalars().all()
        if not jobs:
            return []

        job_texts = [f"{j.title} {j.description or ''}" for j in jobs]
        
        # 4. Generate Machine Learning Semantic Array natively mapped across `jobs`
        content_scores = RecommendationService.calculate_content_match(user_text, job_texts)
        
        # 5. Iteratively assemble the weighted metrics
        recommendations = []
        for idx, job in enumerate(jobs):
            # Breakdown
            score_skills = RecommendationService.calculate_skill_match(user_skills, job.skills_required or [])
            score_content = content_scores[idx]
            score_exp = RecommendationService.calculate_experience_match(user_exp, job.experience_level)
            score_loc = RecommendationService.calculate_location_match(user_locs, remote_pref, job.location, job.is_remote)
            score_salary = RecommendationService.calculate_salary_match(
                profile.expected_salary_min, job.salary_min, job.salary_max
            )
            
            # Hybrid Formula Weights: Skills(35%), Content(25%), Exp(15%), Location(15%), Salary(10%)
            final_score = (
                (score_skills * 0.35) +
                (score_content * 0.25) +
                (score_exp * 0.15) +
                (score_loc * 0.15) +
                (score_salary * 0.10)
            ) * 100.0  # Percentage scale
            
            if final_score >= 40.0:  # Threshold rejection
                # Build dict directly equivalent to Pydantic configuration output
                job_dict = {
                    "id": job.id,
                    "external_id": job.external_id,
                    "title": job.title,
                    "company": job.company,
                    "location": job.location,
                    "description": job.description,
                    "salary_min": job.salary_min,
                    "salary_max": job.salary_max,
                    "currency": job.salary_currency,
                    "is_remote": job.is_remote,
                    "skills_required": job.skills_required,
                    "apply_url": job.apply_url,
                    "posted_at": job.posted_at,
                    "match_score": final_score,
                    "match_breakdown": {
                        "skills": score_skills,
                        "content": score_content,
                        "experience": score_exp,
                        "location": score_loc,
                        "salary": score_salary
                    }
                }
                recommendations.append(job_dict)
                
        # 6. Return strictly sorted Array chopped to Pagination Limits
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        return recommendations[:limit]
