from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from app.models.models import Profile, User, WorkExperience, Education, Certification
from app.schemas.profile import (
    ProfileUpdate,
    WorkExperienceCreate,
    WorkExperienceUpdate,
    EducationCreate,
    EducationUpdate,
    CertificationCreate,
    CertificationUpdate,
)


class ProfileService:
    """
    Business logic encapsulation for User Profiles, including 
    Work Experience, Education, and Certifications CRUD.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_profile(self, user_id: int) -> Profile:
        """
        Retrieves the user's profile with eager loading of all child associations.
        Raises 404 if the profile does not exist.
        """
        stmt = (
            select(Profile)
            .where(Profile.user_id == user_id)
            .options(
                selectinload(Profile.user).selectinload(User.work_experiences),
                selectinload(Profile.user).selectinload(User.educations),
                selectinload(Profile.user).selectinload(User.certifications),
            )
        )
        
        cursor = await self.db.execute(stmt)
        profile = cursor.scalars().first()
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found."
            )
            
        # For Pydantic mapping (`from_attributes=True`), we dynamically attach 
        # the nested elements directly onto the Profile object from the User object
        profile.work_experiences = profile.user.work_experiences
        profile.educations = profile.user.educations
        
        # Sort certifications (since they don't have default order_by in models)
        certs = profile.user.certifications
        profile.certifications = sorted(
            certs, 
            key=lambda c: c.issue_date if c.issue_date else date.min, 
            reverse=True
        )
        
        return profile

    async def update_profile(self, user_id: int, data: ProfileUpdate) -> Profile:
        """
        Updates the root profile metrics and metadata.
        """
        cursor = await self.db.execute(select(Profile).where(Profile.user_id == user_id))
        profile = cursor.scalars().first()
        
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found.")
            
        # Update dynamically provided fields 
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            # Convert HttpUrl formats to standard strings for SQLAlchemy
            if "url" in key and hasattr(value, "__str__"):
                setattr(profile, key, str(value))
            else:
                setattr(profile, key, value)
                
        await self.db.commit()
        await self.db.refresh(profile)
        
        return await self.get_profile(user_id)

    # ── Work Experience CRUD ──────────────────────────────────────────

    async def add_work_experience(self, user_id: int, data: WorkExperienceCreate) -> WorkExperience:
        new_exp = WorkExperience(
            user_id=user_id,
            company_name=data.company_name,
            job_title=data.job_title,
            employment_type=data.employment_type,
            location=data.location,
            start_date=data.start_date,
            end_date=data.end_date,
            is_current=data.is_current,
            description=data.description
        )
        self.db.add(new_exp)
        await self.db.commit()
        await self.db.refresh(new_exp)
        return new_exp

    async def update_work_experience(self, user_id: int, exp_id: int, data: WorkExperienceUpdate) -> WorkExperience:
        exp = await self.db.get(WorkExperience, exp_id)
        if not exp or exp.user_id != user_id:
            raise HTTPException(status_code=404, detail="Work experience not found or unauthorized.")
            
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(exp, key, value)
            
        await self.db.commit()
        await self.db.refresh(exp)
        return exp

    async def delete_work_experience(self, user_id: int, exp_id: int) -> None:
        exp = await self.db.get(WorkExperience, exp_id)
        if not exp or exp.user_id != user_id:
            raise HTTPException(status_code=404, detail="Work experience not found or unauthorized.")
            
        await self.db.delete(exp)
        await self.db.commit()

    # ── Education CRUD ────────────────────────────────────────────────

    async def add_education(self, user_id: int, data: EducationCreate) -> Education:
        new_edu = Education(
            user_id=user_id,
            institution=data.institution,
            degree=data.degree,
            field_of_study=data.field_of_study,
            start_date=data.start_date,
            end_date=data.end_date,
            grade=data.grade,
            activities=data.activities
        )
        self.db.add(new_edu)
        await self.db.commit()
        await self.db.refresh(new_edu)
        return new_edu

    async def update_education(self, user_id: int, edu_id: int, data: EducationUpdate) -> Education:
        edu = await self.db.get(Education, edu_id)
        if not edu or edu.user_id != user_id:
            raise HTTPException(status_code=404, detail="Education not found or unauthorized.")
            
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(edu, key, value)
            
        await self.db.commit()
        await self.db.refresh(edu)
        return edu

    async def delete_education(self, user_id: int, edu_id: int) -> None:
        edu = await self.db.get(Education, edu_id)
        if not edu or edu.user_id != user_id:
            raise HTTPException(status_code=404, detail="Education not found or unauthorized.")
            
        await self.db.delete(edu)
        await self.db.commit()

    # ── Certification CRUD ────────────────────────────────────────────

    async def add_certification(self, user_id: int, data: CertificationCreate) -> Certification:
        new_cert = Certification(
            user_id=user_id,
            name=data.name,
            issuing_organization=data.issuing_organization,
            issue_date=data.issue_date,
            expiry_date=data.expiry_date,
            credential_id=data.credential_id,
            credential_url=str(data.credential_url) if data.credential_url else None
        )
        self.db.add(new_cert)
        await self.db.commit()
        await self.db.refresh(new_cert)
        return new_cert

    async def update_certification(self, user_id: int, cert_id: int, data: CertificationUpdate) -> Certification:
        cert = await self.db.get(Certification, cert_id)
        if not cert or cert.user_id != user_id:
            raise HTTPException(status_code=404, detail="Certification not found or unauthorized.")
            
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key == "credential_url" and value is not None:
                value = str(value)
            setattr(cert, key, value)
            
        await self.db.commit()
        await self.db.refresh(cert)
        return cert

    async def delete_certification(self, user_id: int, cert_id: int) -> None:
        cert = await self.db.get(Certification, cert_id)
        if not cert or cert.user_id != user_id:
            raise HTTPException(status_code=404, detail="Certification not found or unauthorized.")
            
        await self.db.delete(cert)
        await self.db.commit()

    async def _calculate_profile_completion(self, profile: Profile) -> int:
        """
        Dynamically weights missing values establishing profile readiness 0-100 natively.
        """
        score = 0
        if profile.first_name and profile.last_name: score += 15
        if profile.headline or profile.summary: score += 20
        if profile.phone: score += 10
        if profile.location: score += 5
        if profile.resume_url: score += 20
        
        if getattr(profile.user, "work_experiences", False) and len(profile.user.work_experiences) > 0:
            score += 15
        if getattr(profile.user, "educations", False) and len(profile.user.educations) > 0:
            score += 10
        if getattr(profile.user, "skills", False) and len(profile.user.skills) > 0:
            score += 5
            
        return min(score, 100)

    # ── AI Resume Parsing ─────────────────────────────────────────────

    async def upload_and_parse_resume(self, user_id: int, file: "UploadFile") -> dict:
        import os
        import uuid
        import json
        from openai import AsyncOpenAI
        from datetime import datetime
        from fastapi import UploadFile
        
        from app.core.config import settings
        from app.utils.nlp_processor import extract_text_from_pdf
        from app.models.models import Skill, UserSkill, SkillProficiency, WorkExperience, Education

        # 1. Read bytes & configure Storage
        file_bytes = await file.read()
        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            
        filename = f"{uuid.uuid4()}.pdf"
        file_path = os.path.join(upload_dir, filename)
        
        with open(file_path, "wb") as f:
            f.write(file_bytes)
            
        # 2. Attach pathway to Profile
        cursor = await self.db.execute(select(Profile).where(Profile.user_id == user_id).options(
            selectinload(Profile.user).selectinload(User.work_experiences),
            selectinload(Profile.user).selectinload(User.educations),
            selectinload(Profile.user).selectinload(User.skills)
        ))
        profile = cursor.scalars().first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found.")
            
        profile.resume_url = file_path
        
        # 3. ML NLP Extraction
        try:
            raw_text = extract_text_from_pdf(file_bytes)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed parsing PDF: {str(e)}")

        # 4. AsyncOpenAI Prompting (Structured JSON Boundary)
        openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        system_prompt = """
        You are an expert HR Parser. Extract data from the following resume text.
        Return ONLY a strict JSON object mapping natively to these keys:
        {
          "first_name": "string",
          "last_name": "string",
          "phone": "string",
          "summary": "string",
          "skills": ["skill_1", "skill_2"],
          "work_experience": [{"company_name": "str", "job_title": "str", "start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD or null", "description": "str"}],
          "education": [{"institution": "str", "degree": "str"}]
        }
        Leave fields empty or null if they cannot be determined.
        """

        try:
            response = await openai_client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": raw_text[:8000]} # Safe cutoff limits
                ],
                temperature=0.1
            )
            parsed_data = json.loads(response.choices[0].message.content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM parsing failed natively: {str(e)}")

        # 5. Populate Structural Maps
        if parsed_data.get("first_name"): profile.first_name = parsed_data["first_name"]
        if parsed_data.get("last_name"): profile.last_name = parsed_data["last_name"]
        if parsed_data.get("phone"): profile.phone = parsed_data["phone"]
        if parsed_data.get("summary"): profile.summary = parsed_data["summary"]

        # 5a. Skills
        for skill_name in parsed_data.get("skills", []):
            sk = str(skill_name).lower().strip()
            if not sk: continue
            
            stmt_skill = select(Skill).where(Skill.name == sk)
            existing_skill = (await self.db.execute(stmt_skill)).scalars().first()
            if not existing_skill:
                existing_skill = Skill(name=sk, is_trending=False)
                self.db.add(existing_skill)
                await self.db.flush()
                
            stmt_user_skill = select(UserSkill).where(UserSkill.user_id == user_id, UserSkill.skill_id == existing_skill.id)
            if not (await self.db.execute(stmt_user_skill)).scalars().first():
                self.db.add(UserSkill(user_id=user_id, skill_id=existing_skill.id, proficiency=SkillProficiency.intermediate))

        # 5b. Work Experience
        for work in parsed_data.get("work_experience", []):
            if work.get("company_name") and work.get("job_title"):
                start_dt = None
                end_dt = None
                try: 
                    if work.get("start_date"): start_dt = datetime.strptime(str(work["start_date"])[:10], "%Y-%m-%d").date()
                    if work.get("end_date"): end_dt = datetime.strptime(str(work["end_date"])[:10], "%Y-%m-%d").date()
                except ValueError: pass
                
                self.db.add(WorkExperience(
                    user_id=user_id,
                    company_name=work["company_name"],
                    job_title=work["job_title"],
                    description=work.get("description"),
                    start_date=start_dt or datetime(2010, 1, 1).date(),
                    end_date=end_dt,
                    is_current=True if work.get("end_date") in [None, ""] else False
                ))

        # 5c. Education
        for edu in parsed_data.get("education", []):
            if edu.get("institution"):
                self.db.add(Education(
                    user_id=user_id,
                    institution=edu["institution"],
                    degree=edu.get("degree")
                ))

        # 6. Recalculate global profile completion
        profile.profile_completion = await self._calculate_profile_completion(profile)
        
        await self.db.commit()
        return {
            "resume_url": file_path,
            "parsed_profile": parsed_data
        }
