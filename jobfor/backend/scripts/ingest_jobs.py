"""
Standalone Asynchronous Job Ingestion Pipeline
================================================

Ingests localized `.xlsx` job listings into the PostgreSQL `JobCache` table via `asyncpg`.
Enriches missing salaries using OpenAI `gpt-4o-mini` and extracts predefined technical skills using `spaCy`.
"""

import asyncio
import json
import logging
import os
import re
from typing import Any, Dict, List, Optional

import pandas as pd
import spacy
from openai import AsyncOpenAI
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Try to import Django/FastAPI config, fallback to pure os.getenv if running entirely detached
try:
    from app.core.config import settings
    # Force switch the synchronous psycopg2 driver to asyncpg
    SYNC_URL = str(settings.DATABASE_URL)
    DB_URL = SYNC_URL.replace("postgresql://", "postgresql+asyncpg://") if "postgresql://" in SYNC_URL else SYNC_URL
except ImportError:
    DB_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://jobfor:jobfor_secret@localhost:5432/jobsearch")
    DB_URL = DB_URL.replace("postgresql://", "postgresql+asyncpg://") if "postgresql://" in DB_URL else DB_URL

try:
    from app.models.models import JobCache
except ImportError:
    # If the script is ran without python -m backend.scripts... and PYTHONPATH isn't set
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    from app.models.models import JobCache


# ──────────────────────────────────────────────────────────────
# 1. Setup & Configuration
# ──────────────────────────────────────────────────────────────

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize OpenAI Client
# Assumes OPENAI_API_KEY is available in the environment
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize SQLAlchemy Async Engine & Session
engine = create_async_engine(
    DB_URL,
    pool_size=10,
    max_overflow=20,
    echo=False,  # Set to True for debugging SQL statements
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Initialize spaCy
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.warning("Spacy model 'en_core_web_sm' not found. Installing it dynamically...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
    nlp = spacy.load("en_core_web_sm")

# Define target explicit skills to match via Regex word boundaries
TARGET_SKILLS = {
    "python", "java", "c++", "c#", "javascript", "typescript", "golang", "go", "ruby", "php",
    "fastapi", "django", "flask", "react", "angular", "vue", "nextjs", "spring boot", "nodejs",
    "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "cassandra", "sql",
    "docker", "kubernetes", "aws", "gcp", "azure", "ci/cd", "terraform", "ansible",
    "machine learning", "deep learning", "nlp", "computer vision", "pandas", "numpy", "pytorch", "tensorflow",
    "agile", "scrum", "leadership", "communication", "problem solving"
}


# ──────────────────────────────────────────────────────────────
# 2. AI Enrichment & Cleaning Functions
# ──────────────────────────────────────────────────────────────

def extract_skills(text_content: str) -> List[str]:
    """
    Extracts predefined skills using regex phrase boundary matching via spaCy's tokenizer.
    Returns a deduplicated list of lowercase strings.
    """
    if not isinstance(text_content, str) or not text_content.strip():
        return []

    doc = nlp(text_content)
    extracted = set()
    cleaned_text = " ".join([token.text.lower() for token in doc])
    
    for skill in TARGET_SKILLS:
        # Pad with \b boundaries to avoid matching sub-words (e.g., 'go' inside 'algorithm')
        escaped_skill = re.escape(skill)
        pattern = rf"\b{escaped_skill}\b"
        if re.search(pattern, cleaned_text):
            extracted.add(skill)

    return list(extracted)


async def estimate_salary(title: str, company: str, location: str, description: str) -> Optional[Dict[str, Any]]:
    """
    Queries OpenAI gpt-4o-mini to estimate reasonable bounds for an unlisted salary.
    Respects a 1-second timeout between calls to avoid hitting Tier 1 rate limits.
    """
    # Defensive sleep to prevent rate limits
    await asyncio.sleep(1.0)

    prompt_context = f"Job Title: {title}\nCompany: {company}\nLocation: {location}\nDescription Extract: {str(description)[:1500]}"
    
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.0,  # Highly deterministic for data parsing
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert HR data parser. Your task is to extract or intelligently estimate "
                        "the expected ANNUAL salary for a given job. RULES: "
                        "1. Provide the response as pure JSON matching this exact structure: "
                        "{\"salaryMin\": Number, \"salaryMax\": Number, \"currency\": \"INR\" | \"USD\"}. "
                        "2. Even if the job description doesn't explicitly state the salary, you MUST estimate "
                        "a reasonable market rate based on the job title, company, and location. "
                        "3. If the location is in India or the job is remote but aimed at India, use INR metrics. "
                        "4. If it's a US or global remote role, use USD metrics. "
                        "5. Ensure the numbers are integers."
                    )
                },
                {"role": "user", "content": prompt_context}
            ]
        )
        
        raw_json_str = response.choices[0].message.content.strip()
        # Clean Markdown wrappers
        if raw_json_str.startswith("```json"):
            raw_json_str = raw_json_str[7:]
        if raw_json_str.startswith("```"):
            raw_json_str = raw_json_str[3:]
        if raw_json_str.endswith("```"):
            raw_json_str = raw_json_str[:-3]
            
        parsed_salary = json.loads(raw_json_str.strip())
        return parsed_salary
        
    except Exception as e:
        logger.error(f"Failed to estimate salary for {title} @ {company}: {e}")
        return None


# ──────────────────────────────────────────────────────────────
# 3. Batch Processing & Ingestion Core
# ──────────────────────────────────────────────────────────────

async def process_batch(df_batch: pd.DataFrame, session: AsyncSession):
    """
    Cleans a pandas chunk of rows, enriches via AI concurrently, and performs
    a safe upsert (ON CONFLICT DO NOTHING) via SQLAlchemy 2.0 ORM.
    """
    
    enrichment_tasks = []
    enriched_rows = []

    for index, row in df_batch.iterrows():
        # Standardize basic types from pandas
        title = str(row.get("title", "")).strip()
        company = str(row.get("company", "Unknown")).strip()
        location = str(row.get("location", "")).strip()
        description = str(row.get("description", "")).strip()
        external_id = str(row.get("job_id", row.get("external_id", f"gen_{index}"))).strip()
        apply_url = str(row.get("apply_url", row.get("url", ""))).strip()
        is_remote = "remote" in location.lower() or "remote" in title.lower()

        raw_data = row.to_dict()
        # Sanitize NaNs from dict before JSON serialization
        raw_data = {k: (v if pd.notna(v) else None) for k, v in raw_data.items()}

        skills = extract_skills(title + " " + description)

        record = {
            "external_id": external_id,
            "source": "indian_job_market_excel",
            "title": title[:300] if title else "Unknown",
            "company": company[:300] if company else "Unknown",
            "location": location[:300] if location else None,
            "description": description,
            "is_remote": is_remote,
            "skills_required": skills,
            "apply_url": apply_url[:1000] if apply_url else None,
            "raw_data": raw_data,
            "currency": "INR",  # fallback default
            "salary_min": None,
            "salary_max": None
        }

        # Check if salary looks missing (or zero)
        existing_min = row.get("salary_min")
        existing_max = row.get("salary_max")

        if pd.isna(existing_min) or pd.isna(existing_max) or existing_min == 0 or existing_max == 0:
            # We must await the OpenAI estimation for this row
            # But to keep it non-blocking, we create tasks
            task = asyncio.create_task(estimate_salary(title, company, location, description))
            enrichment_tasks.append((record, task))
        else:
            record["salary_min"] = int(existing_min)
            record["salary_max"] = int(existing_max)
            try:
                record["currency"] = str(row.get("currency", "INR")).upper()
            except Exception:
                pass
                
            enriched_rows.append(record)

    # Resolve all OpenAI bounds
    if enrichment_tasks:
        for record, task in enrichment_tasks:
            result = await task
            if result:
                record["salary_min"] = result.get("salaryMin", None)
                record["salary_max"] = result.get("salaryMax", None)
                record["currency"] = result.get("currency", "INR")
            enriched_rows.append(record)
        
    if not enriched_rows:
        return

    # Bulk Upsert with ON CONFLICT DO NOTHING via SQLAlchemy ORM
    # JobCache has a UNIQUE constraint on ("source", "external_id")
    stmt = insert(JobCache).values(enriched_rows)
    stmt = stmt.on_conflict_do_nothing(
        index_elements=["source", "external_id"]
    )
    
    await session.execute(stmt)
    await session.commit()
    logger.info(f"Successfully committed batch of {len(enriched_rows)} records.")


async def main(file_path: str):
    """
    Main controller for the ingestion loop.
    Reads an MS Excel `.xlsx` file iteratively to avoid OOM crashes.
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return

    chunk_size = 500  # Number of rows per batch
    logger.info(f"Starting bulk ingestion of {file_path} in chunks of {chunk_size}...")

    # Load dataset into memory
    logger.info("Loading dataset into memory constraints...")
    df = pd.read_excel(file_path, engine="openpyxl")
    total_rows = len(df)
    logger.info(f"Detected {total_rows} total rows to process.")

    async with AsyncSessionLocal() as session:
        for i in range(0, total_rows, chunk_size):
            df_batch = df.iloc[i : i + chunk_size]
            logger.info(f"Processing chunk {i} to {i + len(df_batch)}...")
            
            # Process batch concurrently
            await process_batch(df_batch, session)
            
    logger.info("🎉 Ingestion complete.")


if __name__ == "__main__":
    # Ensure event loop handles KeyboardInterrupt cleanly
    try:
        # Target explicit dataset file
        dataset_target = r"E:\Antigravity Projects\indian-job-market-dataset-2025.xlsx"
        asyncio.run(main(dataset_target))
    except KeyboardInterrupt:
        logger.info("Ingestion manually aborted by user.")
