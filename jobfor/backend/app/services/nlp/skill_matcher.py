"""
app/services/nlp/skill_matcher.py — Canonical Skill Extraction
===============================================================
`SkillMatcher` resolves raw text phrases to canonical skill names
from the `skills` database table.

Matching strategy (applied in priority order):
  1. Exact match against `skill.name` (lowercased)
  2. Alias match against `skill.aliases` JSONB array entries
  3. Substring match — candidate phrase contains a known skill name
  4. Fuzzy match (RapidFuzz ≥ 85 score) for typo tolerance

The matcher loads the skill catalogue once and caches it in memory,
with a `refresh()` method for long-running processes.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

try:
    from rapidfuzz import fuzz, process as rf_process
    _RAPIDFUZZ_AVAILABLE = True
except ImportError:
    _RAPIDFUZZ_AVAILABLE = False
    logger.warning(
        "rapidfuzz not installed — fuzzy skill matching disabled. "
        "Run: pip install rapidfuzz"
    )


@dataclass
class SkillMatch:
    """A resolved skill match with its canonical name and confidence score."""
    canonical_name: str
    match_type: str          # "exact" | "alias" | "substring" | "fuzzy"
    score: float             # 0.0–1.0 confidence


@dataclass
class _SkillRecord:
    """Internal in-memory representation of a Skill row."""
    name: str                                    # canonical lowercase
    aliases: list[str] = field(default_factory=list)


class SkillMatcher:
    """
    Match free-text candidate phrases to canonical skill names.

    Usage::

        async with async_db_session() as db:
            matcher = SkillMatcher()
            await matcher.load(db)

        matches = matcher.match_phrases(["python", "machine learning", "pytohn"])
        canonical = [m.canonical_name for m in matches]
    """

    # Minimum fuzzy score (0–100) to accept a fuzzy match
    FUZZY_THRESHOLD: int = 85

    def __init__(self) -> None:
        self._skills: list[_SkillRecord] = []
        self._name_index: dict[str, str] = {}        # lowercase_name → canonical
        self._alias_index: dict[str, str] = {}       # lowercase_alias → canonical
        self._loaded: bool = False

    # ── Lifecycle ─────────────────────────────────────────────────

    async def load(self, db: AsyncSession) -> None:
        """
        Load all skills from the database into memory.

        Must be called once before `match_phrases()`.
        Re-calling refreshes the cache (useful for long-running scripts).
        """
        from app.models.models import Skill  # local import avoids circular deps

        result = await db.execute(
            select(Skill.name, Skill.aliases).where(Skill.name.isnot(None))
        )
        rows = result.all()

        self._skills.clear()
        self._name_index.clear()
        self._alias_index.clear()

        for name, aliases in rows:
            canonical = name.lower().strip()
            record = _SkillRecord(
                name=canonical,
                aliases=[a.lower().strip() for a in (aliases or [])],
            )
            self._skills.append(record)
            self._name_index[canonical] = canonical

            for alias in record.aliases:
                self._alias_index[alias] = canonical

        self._loaded = True
        logger.info(
            "SkillMatcher loaded %d canonical skills (%d aliases).",
            len(self._skills),
            len(self._alias_index),
        )

    def refresh(self) -> None:
        """Mark cache as stale — next `load()` call will rebuild it."""
        self._loaded = False

    # ── Public API ────────────────────────────────────────────────

    def match_phrases(self, phrases: Sequence[str]) -> list[SkillMatch]:
        """
        Resolve a list of candidate phrases to canonical skill matches.

        Deduplicates results: each canonical skill name appears at most once.
        """
        if not self._loaded:
            raise RuntimeError("Call `await matcher.load(db)` before matching.")

        resolved: dict[str, SkillMatch] = {}

        for phrase in phrases:
            phrase = phrase.lower().strip()
            if not phrase or len(phrase) < 2:
                continue

            match = (
                self._exact_match(phrase)
                or self._alias_match(phrase)
                or self._substring_match(phrase)
                or (self._fuzzy_match(phrase) if _RAPIDFUZZ_AVAILABLE else None)
            )

            if match and match.canonical_name not in resolved:
                resolved[match.canonical_name] = match

        return list(resolved.values())

    def extract_skill_names(self, phrases: Sequence[str]) -> list[str]:
        """Convenience wrapper — returns just the canonical names."""
        return [m.canonical_name for m in self.match_phrases(phrases)]

    # ── Matching strategies ───────────────────────────────────────

    def _exact_match(self, phrase: str) -> SkillMatch | None:
        if phrase in self._name_index:
            return SkillMatch(
                canonical_name=self._name_index[phrase],
                match_type="exact",
                score=1.0,
            )
        return None

    def _alias_match(self, phrase: str) -> SkillMatch | None:
        if phrase in self._alias_index:
            return SkillMatch(
                canonical_name=self._alias_index[phrase],
                match_type="alias",
                score=0.95,
            )
        return None

    def _substring_match(self, phrase: str) -> SkillMatch | None:
        """Match if the phrase *contains* an exact skill name as a whole word."""
        for canonical in self._name_index:
            # Use word-boundary regex to avoid 'java' matching 'javascript'
            if re.search(r"\b" + re.escape(canonical) + r"\b", phrase):
                return SkillMatch(
                    canonical_name=canonical,
                    match_type="substring",
                    score=0.85,
                )
        return None

    def _fuzzy_match(self, phrase: str) -> SkillMatch | None:
        """RapidFuzz token_sort_ratio against all canonical names."""
        if not self._skills:
            return None

        candidates = list(self._name_index.keys())
        result = rf_process.extractOne(
            phrase,
            candidates,
            scorer=fuzz.token_sort_ratio,
            score_cutoff=self.FUZZY_THRESHOLD,
        )
        if result:
            matched_name, score, _ = result
            return SkillMatch(
                canonical_name=self._name_index[matched_name],
                match_type="fuzzy",
                score=score / 100.0,
            )
        return None
