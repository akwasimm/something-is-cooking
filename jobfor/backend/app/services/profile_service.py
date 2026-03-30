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

    # ── AI Resume Parsing ─────────────────────────────────────────────

    async def upload_and_parse_resume(self, user_id: int, file: "UploadFile") -> dict:
        import os
        import uuid
        from fastapi import UploadFile
        from app.utils.nlp_processor import extract_text_from_pdf, extract_skills_from_text
        from app.models.models import Skill, UserSkill, SkillProficiency

        # 1. Read bytes
        file_bytes = await file.read()
        
        # 2. Local File System Management
        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            
        filename = f"{uuid.uuid4()}.pdf"
        file_path = os.path.join(upload_dir, filename)
        
        with open(file_path, "wb") as f:
            f.write(file_bytes)
            
        # 3. Attach pathway to Profile
        cursor = await self.db.execute(select(Profile).where(Profile.user_id == user_id))
        profile = cursor.scalars().first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found.")
            
        profile.resume_url = file_path
        await self.db.commit()

        # 4. Invoke the ML extraction loops natively
        try:
            raw_text = extract_text_from_pdf(file_bytes)
            found_skills = extract_skills_from_text(raw_text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed parsing PDF: {str(e)}")
            
        # 5. Iteratively associate newly mapped traits to the User profile
        for skill_name in found_skills:
            # Upsert into structural Skill mapping
            stmt_skill = select(Skill).where(Skill.name == skill_name)
            s_cursor = await self.db.execute(stmt_skill)
            existing_skill = s_cursor.scalars().first()
            
            if not existing_skill:
                existing_skill = Skill(name=skill_name, is_trending=False)
                self.db.add(existing_skill)
                await self.db.flush()
                
            # Upsert into UserSkill binding
            stmt_user_skill = select(UserSkill).where(
                UserSkill.user_id == user_id, 
                UserSkill.skill_id == existing_skill.id
            )
            us_cursor = await self.db.execute(stmt_user_skill)
            if not us_cursor.scalars().first():
                new_binding = UserSkill(
                    user_id=user_id,
                    skill_id=existing_skill.id,
                    proficiency=SkillProficiency.intermediate
                )
                self.db.add(new_binding)
                
        await self.db.commit()
        
        return {
            "resume_url": file_path,
            "extracted_skills": found_skills
        }
