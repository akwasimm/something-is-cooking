"""
scripts/seed.py — Master Skills Seed Script
=============================================
Populates the `skills` table with a curated set of canonical skills
used by the NLP pipeline, SkillMatcher, and the frontend tag system.

Features:
  • Async SQLAlchemy 2.0 session via async_db_session()
  • Idempotent — skips any skill that already exists (checks by name)
  • Structured skill catalogue with categories, aliases, and trending flags
  • Demand scores (0.0–1.0) seeded from industry data estimates

Usage::

    # From the backend/ directory:
    python scripts/seed.py

    # Preview without writing (dry-run):
    python scripts/seed.py --dry-run

    # Reset and re-seed (deletes existing skills first):
    python scripts/seed.py --reset
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from pathlib import Path
from typing import Any

# ── Make `app` importable when running from scripts/ ───────────
_BACKEND_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BACKEND_ROOT))

from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.core.async_database import async_db_session, verify_async_connection
from app.models.models import Skill

# ── Logging ────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("seed")


# ══════════════════════════════════════════════════════════════════════════════
# Master Skill Catalogue
# ══════════════════════════════════════════════════════════════════════════════

SKILLS: list[dict[str, Any]] = [

    # ── Programming Languages ──────────────────────────────────
    {
        "name": "python",
        "category": "Programming Language",
        "aliases": ["py", "python3", "python2"],
        "is_trending": True,
        "demand_score": 0.97,
    },
    {
        "name": "javascript",
        "category": "Programming Language",
        "aliases": ["js", "javascript es6", "ecmascript"],
        "is_trending": True,
        "demand_score": 0.98,
    },
    {
        "name": "typescript",
        "category": "Programming Language",
        "aliases": ["ts", "typescript js"],
        "is_trending": True,
        "demand_score": 0.91,
    },
    {
        "name": "java",
        "category": "Programming Language",
        "aliases": ["java8", "java11", "java17", "jdk"],
        "is_trending": False,
        "demand_score": 0.85,
    },
    {
        "name": "go",
        "category": "Programming Language",
        "aliases": ["golang"],
        "is_trending": True,
        "demand_score": 0.82,
    },
    {
        "name": "rust",
        "category": "Programming Language",
        "aliases": ["rust-lang"],
        "is_trending": True,
        "demand_score": 0.72,
    },
    {
        "name": "c++",
        "category": "Programming Language",
        "aliases": ["cpp", "c plus plus"],
        "is_trending": False,
        "demand_score": 0.75,
    },
    {
        "name": "c#",
        "category": "Programming Language",
        "aliases": ["csharp", "c sharp", "dotnet c#"],
        "is_trending": False,
        "demand_score": 0.74,
    },
    {
        "name": "php",
        "category": "Programming Language",
        "aliases": ["php8", "php7"],
        "is_trending": False,
        "demand_score": 0.62,
    },
    {
        "name": "kotlin",
        "category": "Programming Language",
        "aliases": ["kotlin android"],
        "is_trending": True,
        "demand_score": 0.76,
    },
    {
        "name": "swift",
        "category": "Programming Language",
        "aliases": ["swift ios", "apple swift"],
        "is_trending": False,
        "demand_score": 0.65,
    },
    {
        "name": "ruby",
        "category": "Programming Language",
        "aliases": ["ruby on rails", "ror"],
        "is_trending": False,
        "demand_score": 0.55,
    },
    {
        "name": "scala",
        "category": "Programming Language",
        "aliases": ["scala spark"],
        "is_trending": False,
        "demand_score": 0.60,
    },
    {
        "name": "r",
        "category": "Programming Language",
        "aliases": ["r language", "r programming", "rstats"],
        "is_trending": False,
        "demand_score": 0.58,
    },
    {
        "name": "sql",
        "category": "Programming Language",
        "aliases": ["structured query language", "t-sql", "pl/sql"],
        "is_trending": False,
        "demand_score": 0.92,
    },

    # ── Web Frameworks ──────────────────────────────────────────
    {
        "name": "react",
        "category": "Frontend Framework",
        "aliases": ["reactjs", "react.js", "react js"],
        "is_trending": True,
        "demand_score": 0.95,
    },
    {
        "name": "next.js",
        "category": "Frontend Framework",
        "aliases": ["nextjs", "next js"],
        "is_trending": True,
        "demand_score": 0.88,
    },
    {
        "name": "vue.js",
        "category": "Frontend Framework",
        "aliases": ["vuejs", "vue js", "vue"],
        "is_trending": True,
        "demand_score": 0.78,
    },
    {
        "name": "angular",
        "category": "Frontend Framework",
        "aliases": ["angularjs", "angular2+"],
        "is_trending": False,
        "demand_score": 0.72,
    },
    {
        "name": "svelte",
        "category": "Frontend Framework",
        "aliases": ["sveltekit"],
        "is_trending": True,
        "demand_score": 0.65,
    },

    # ── Backend Frameworks ──────────────────────────────────────
    {
        "name": "node.js",
        "category": "Backend Framework",
        "aliases": ["nodejs", "node js", "node"],
        "is_trending": True,
        "demand_score": 0.90,
    },
    {
        "name": "fastapi",
        "category": "Backend Framework",
        "aliases": ["fast api", "fastapi python"],
        "is_trending": True,
        "demand_score": 0.87,
    },
    {
        "name": "django",
        "category": "Backend Framework",
        "aliases": ["django rest framework", "drf"],
        "is_trending": False,
        "demand_score": 0.80,
    },
    {
        "name": "flask",
        "category": "Backend Framework",
        "aliases": ["flask python", "flask api"],
        "is_trending": False,
        "demand_score": 0.72,
    },
    {
        "name": "express.js",
        "category": "Backend Framework",
        "aliases": ["expressjs", "express js", "express"],
        "is_trending": False,
        "demand_score": 0.78,
    },
    {
        "name": "spring boot",
        "category": "Backend Framework",
        "aliases": ["spring", "springboot", "spring framework"],
        "is_trending": False,
        "demand_score": 0.76,
    },
    {
        "name": ".net",
        "category": "Backend Framework",
        "aliases": ["dotnet", "asp.net", "asp.net core"],
        "is_trending": False,
        "demand_score": 0.70,
    },

    # ── Databases ───────────────────────────────────────────────
    {
        "name": "postgresql",
        "category": "Database",
        "aliases": ["postgres", "psql", "pg"],
        "is_trending": True,
        "demand_score": 0.88,
    },
    {
        "name": "mysql",
        "category": "Database",
        "aliases": ["mysql db", "mysql server"],
        "is_trending": False,
        "demand_score": 0.78,
    },
    {
        "name": "mongodb",
        "category": "Database",
        "aliases": ["mongo", "mongo db"],
        "is_trending": True,
        "demand_score": 0.80,
    },
    {
        "name": "redis",
        "category": "Database",
        "aliases": ["redis cache", "redis db"],
        "is_trending": True,
        "demand_score": 0.82,
    },
    {
        "name": "elasticsearch",
        "category": "Database",
        "aliases": ["elastic search", "elastic", "es"],
        "is_trending": True,
        "demand_score": 0.79,
    },
    {
        "name": "cassandra",
        "category": "Database",
        "aliases": ["apache cassandra"],
        "is_trending": False,
        "demand_score": 0.60,
    },
    {
        "name": "sqlite",
        "category": "Database",
        "aliases": ["sqlite3"],
        "is_trending": False,
        "demand_score": 0.55,
    },
    {
        "name": "dynamodb",
        "category": "Database",
        "aliases": ["aws dynamodb", "amazon dynamodb"],
        "is_trending": False,
        "demand_score": 0.68,
    },
    {
        "name": "firebase",
        "category": "Database",
        "aliases": ["firebase realtime", "firestore"],
        "is_trending": True,
        "demand_score": 0.70,
    },
    {
        "name": "supabase",
        "category": "Database",
        "aliases": [],
        "is_trending": True,
        "demand_score": 0.72,
    },

    # ── Cloud Platforms ─────────────────────────────────────────
    {
        "name": "aws",
        "category": "Cloud Platform",
        "aliases": ["amazon web services", "amazon aws"],
        "is_trending": True,
        "demand_score": 0.95,
    },
    {
        "name": "google cloud",
        "category": "Cloud Platform",
        "aliases": ["gcp", "google cloud platform", "google cloud services"],
        "is_trending": True,
        "demand_score": 0.85,
    },
    {
        "name": "azure",
        "category": "Cloud Platform",
        "aliases": ["microsoft azure", "ms azure"],
        "is_trending": True,
        "demand_score": 0.88,
    },

    # ── DevOps & Infrastructure ─────────────────────────────────
    {
        "name": "docker",
        "category": "DevOps",
        "aliases": ["docker container", "docker compose", "containerization"],
        "is_trending": True,
        "demand_score": 0.93,
    },
    {
        "name": "kubernetes",
        "category": "DevOps",
        "aliases": ["k8s", "kube", "k8"],
        "is_trending": True,
        "demand_score": 0.88,
    },
    {
        "name": "terraform",
        "category": "DevOps",
        "aliases": ["terraform iac", "hashicorp terraform"],
        "is_trending": True,
        "demand_score": 0.84,
    },
    {
        "name": "ansible",
        "category": "DevOps",
        "aliases": ["ansible automation"],
        "is_trending": False,
        "demand_score": 0.70,
    },
    {
        "name": "jenkins",
        "category": "DevOps",
        "aliases": ["jenkins ci", "jenkins pipeline"],
        "is_trending": False,
        "demand_score": 0.68,
    },
    {
        "name": "github actions",
        "category": "DevOps",
        "aliases": ["gh actions", "github ci"],
        "is_trending": True,
        "demand_score": 0.85,
    },
    {
        "name": "gitlab ci",
        "category": "DevOps",
        "aliases": ["gitlab pipeline", "gitlab cicd"],
        "is_trending": True,
        "demand_score": 0.78,
    },
    {
        "name": "linux",
        "category": "DevOps",
        "aliases": ["unix", "bash", "shell scripting"],
        "is_trending": False,
        "demand_score": 0.88,
    },
    {
        "name": "nginx",
        "category": "DevOps",
        "aliases": ["nginx server"],
        "is_trending": False,
        "demand_score": 0.72,
    },

    # ── Machine Learning & Data Science ────────────────────────
    {
        "name": "machine learning",
        "category": "AI / ML",
        "aliases": ["ml", "machine-learning", "supervised learning"],
        "is_trending": True,
        "demand_score": 0.93,
    },
    {
        "name": "deep learning",
        "category": "AI / ML",
        "aliases": ["deep neural networks", "neural networks", "dl"],
        "is_trending": True,
        "demand_score": 0.88,
    },
    {
        "name": "natural language processing",
        "category": "AI / ML",
        "aliases": ["nlp", "text mining", "language models"],
        "is_trending": True,
        "demand_score": 0.87,
    },
    {
        "name": "computer vision",
        "category": "AI / ML",
        "aliases": ["cv", "image recognition", "object detection"],
        "is_trending": True,
        "demand_score": 0.85,
    },
    {
        "name": "pytorch",
        "category": "AI / ML",
        "aliases": ["torch", "pytorch framework"],
        "is_trending": True,
        "demand_score": 0.87,
    },
    {
        "name": "tensorflow",
        "category": "AI / ML",
        "aliases": ["tf", "tensorflow2", "keras"],
        "is_trending": True,
        "demand_score": 0.84,
    },
    {
        "name": "scikit-learn",
        "category": "AI / ML",
        "aliases": ["sklearn", "scikit learn"],
        "is_trending": False,
        "demand_score": 0.82,
    },
    {
        "name": "pandas",
        "category": "Data Science",
        "aliases": ["pandas python", "pd"],
        "is_trending": False,
        "demand_score": 0.85,
    },
    {
        "name": "numpy",
        "category": "Data Science",
        "aliases": ["np", "numpy python"],
        "is_trending": False,
        "demand_score": 0.82,
    },
    {
        "name": "apache spark",
        "category": "Data Engineering",
        "aliases": ["spark", "pyspark", "spark streaming"],
        "is_trending": True,
        "demand_score": 0.80,
    },
    {
        "name": "apache kafka",
        "category": "Data Engineering",
        "aliases": ["kafka", "kafka streaming"],
        "is_trending": True,
        "demand_score": 0.79,
    },
    {
        "name": "airflow",
        "category": "Data Engineering",
        "aliases": ["apache airflow", "airflow dag"],
        "is_trending": True,
        "demand_score": 0.78,
    },
    {
        "name": "dbt",
        "category": "Data Engineering",
        "aliases": ["data build tool", "dbt core"],
        "is_trending": True,
        "demand_score": 0.76,
    },
    {
        "name": "llm",
        "category": "AI / ML",
        "aliases": ["large language model", "gpt", "openai", "chatgpt"],
        "is_trending": True,
        "demand_score": 0.92,
    },
    {
        "name": "langchain",
        "category": "AI / ML",
        "aliases": ["lang chain"],
        "is_trending": True,
        "demand_score": 0.85,
    },

    # ── Mobile ──────────────────────────────────────────────────
    {
        "name": "react native",
        "category": "Mobile",
        "aliases": ["rn", "react-native"],
        "is_trending": True,
        "demand_score": 0.80,
    },
    {
        "name": "flutter",
        "category": "Mobile",
        "aliases": ["dart flutter", "flutter dart"],
        "is_trending": True,
        "demand_score": 0.80,
    },
    {
        "name": "android",
        "category": "Mobile",
        "aliases": ["android sdk", "android development"],
        "is_trending": False,
        "demand_score": 0.72,
    },
    {
        "name": "ios",
        "category": "Mobile",
        "aliases": ["ios development", "xcode", "uikit"],
        "is_trending": False,
        "demand_score": 0.68,
    },

    # ── Tools & Practices ───────────────────────────────────────
    {
        "name": "git",
        "category": "Tools",
        "aliases": ["version control", "github", "gitlab", "git version control"],
        "is_trending": False,
        "demand_score": 0.95,
    },
    {
        "name": "rest api",
        "category": "Architecture",
        "aliases": ["restful", "rest", "restful api", "http api"],
        "is_trending": False,
        "demand_score": 0.92,
    },
    {
        "name": "graphql",
        "category": "Architecture",
        "aliases": ["graph ql"],
        "is_trending": True,
        "demand_score": 0.78,
    },
    {
        "name": "microservices",
        "category": "Architecture",
        "aliases": ["micro services", "microservice architecture"],
        "is_trending": True,
        "demand_score": 0.85,
    },
    {
        "name": "agile",
        "category": "Methodology",
        "aliases": ["scrum", "kanban", "agile scrum"],
        "is_trending": False,
        "demand_score": 0.80,
    },
    {
        "name": "ci/cd",
        "category": "DevOps",
        "aliases": ["continuous integration", "continuous delivery", "cicd pipeline"],
        "is_trending": True,
        "demand_score": 0.88,
    },
    {
        "name": "system design",
        "category": "Architecture",
        "aliases": ["distributed systems", "high level design", "hld"],
        "is_trending": False,
        "demand_score": 0.85,
    },

    # ── Testing ─────────────────────────────────────────────────
    {
        "name": "pytest",
        "category": "Testing",
        "aliases": ["py test"],
        "is_trending": True,
        "demand_score": 0.78,
    },
    {
        "name": "jest",
        "category": "Testing",
        "aliases": ["jest js"],
        "is_trending": True,
        "demand_score": 0.76,
    },
    {
        "name": "selenium",
        "category": "Testing",
        "aliases": ["selenium webdriver"],
        "is_trending": False,
        "demand_score": 0.65,
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# Seed functions
# ══════════════════════════════════════════════════════════════════════════════

async def seed_skills(dry_run: bool = False, reset: bool = False) -> None:
    """
    Insert master skills into the `skills` table.

    Parameters
    ----------
    dry_run : If True, print what would be inserted but do not commit.
    reset   : If True, delete all existing skills before inserting.
    """
    log.info("=" * 60)
    log.info("  JobFor Skill Seeder")
    log.info("=" * 60)

    if not await verify_async_connection():
        log.critical("❌ Cannot connect to PostgreSQL.")
        sys.exit(1)

    async with async_db_session() as db:

        # ── Optional reset ─────────────────────────────────────
        if reset and not dry_run:
            log.warning("⚠️  --reset: deleting all existing skills…")
            await db.execute(delete(Skill))
            await db.commit()
            log.info("Existing skills cleared.")

        # ── Fetch existing skill names ─────────────────────────
        result = await db.execute(select(Skill.name))
        existing: set[str] = {row[0].lower() for row in result.all()}
        log.info("Existing skills in DB: %d", len(existing))

        # ── Classify skills ────────────────────────────────────
        to_insert: list[dict] = []
        skipped: list[str] = []

        for skill in SKILLS:
            name_lower = skill["name"].lower()
            if name_lower in existing:
                skipped.append(skill["name"])
            else:
                to_insert.append(skill)

        log.info(
            "Skills to insert: %d | Already exist (skipped): %d",
            len(to_insert),
            len(skipped),
        )

        if skipped:
            log.debug("Skipped: %s", ", ".join(skipped))

        if not to_insert:
            log.info("✅ All skills already exist. Nothing to seed.")
            return

        # ── Dry-run preview ────────────────────────────────────
        if dry_run:
            log.info("DRY-RUN — skills that would be inserted:")
            for s in to_insert:
                log.info(
                    "  • %-35s [%s] trending=%s demand=%.2f",
                    s["name"], s["category"], s["is_trending"], s["demand_score"] or 0,
                )
            return

        # ── Bulk upsert ────────────────────────────────────────
        stmt = pg_insert(Skill).values(to_insert)
        stmt = stmt.on_conflict_do_nothing(index_elements=["name"])
        await db.execute(stmt)
        await db.commit()

        log.info("✅ Inserted %d new skills into the database.", len(to_insert))

        # ── Summary by category ────────────────────────────────
        by_cat: dict[str, int] = {}
        for s in to_insert:
            cat = s.get("category", "Uncategorised")
            by_cat[cat] = by_cat.get(cat, 0) + 1

        log.info("Breakdown by category:")
        for cat, count in sorted(by_cat.items()):
            log.info("  %-35s %d skills", cat, count)


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="seed",
        description="Seed the JobFor skills master table.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview inserts without writing to the database.",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete all existing skills before seeding (destructive!).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    asyncio.run(seed_skills(dry_run=args.dry_run, reset=args.reset))


if __name__ == "__main__":
    main()
