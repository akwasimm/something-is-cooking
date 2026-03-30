"""
app/services/nlp/preprocessor.py — Text Preprocessing Pipeline
===============================================================
`TextPreprocessor` wraps a spaCy `nlp` pipeline and exposes clean
text-processing primitives used by `SkillMatcher` and other NLP tasks.

Responsibilities:
  - Tokenization, lemmatization, stop-word removal
  - Named-entity recognition (ORG, PRODUCT) for company/tech-name hints
  - Noun-chunk extraction for compound skill phrases (e.g. "machine learning")
  - Sentence segmentation for structured section detection
"""

from __future__ import annotations

import logging
import re
import string
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Iterable

import spacy
from spacy.language import Language
from spacy.tokens import Doc, Span, Token

logger = logging.getLogger(__name__)

# Extra domain-specific stop words that add noise in skill extraction
_DOMAIN_STOP_WORDS: frozenset[str] = frozenset(
    {
        "experience", "knowledge", "understanding", "familiarity",
        "ability", "skill", "skills", "proficiency", "hands", "on",
        "must", "should", "preferred", "plus", "bonus", "excellent",
        "strong", "year", "years", "month", "months", "good", "great",
        "team", "work", "working", "role", "position", "job", "company",
    }
)


@dataclass
class ProcessedText:
    """Container for all artefacts produced by `TextPreprocessor.process()`."""

    raw: str
    cleaned: str
    tokens: list[str] = field(default_factory=list)          # lemmatised, lowercased
    noun_chunks: list[str] = field(default_factory=list)     # multi-word phrases
    entities: list[tuple[str, str]] = field(default_factory=list)  # (text, label)
    sentences: list[str] = field(default_factory=list)


@lru_cache(maxsize=1)
def _load_spacy_model() -> Language:
    """
    Load and cache the spaCy model.

    Falls back to `en_core_web_sm` if the larger `en_core_web_md`
    model is not installed — md gives better NER for tech entities.
    """
    for model_name in ("en_core_web_md", "en_core_web_sm"):
        try:
            nlp = spacy.load(model_name)
            logger.info("spaCy model loaded: %s", model_name)
            return nlp
        except OSError:
            continue

    raise RuntimeError(
        "No spaCy model found. Run:\n"
        "  python -m spacy download en_core_web_md\n"
        "  # or: python -m spacy download en_core_web_sm"
    )


class TextPreprocessor:
    """
    Lightweight NLP pre-processing pipeline for job description text.

    Examples
    --------
    >>> proc = TextPreprocessor()
    >>> result = proc.process("Requires 3+ years of Python and AWS experience.")
    >>> result.tokens
    ['require', 'year', 'python', 'aws', 'experience']
    >>> result.noun_chunks
    ['python', 'aws experience']
    """

    # Regex patterns
    _URL_RE = re.compile(r"https?://\S+|www\.\S+")
    _EMAIL_RE = re.compile(r"\S+@\S+\.\S+")
    _BULLET_RE = re.compile(r"^[\•\-\*\>\·]\s*", re.MULTILINE)
    _WHITESPACE_RE = re.compile(r"\s{2,}")
    _PUNCT_RE = re.compile(r"[%s]" % re.escape(string.punctuation.replace("+", "").replace("#", "")))

    def __init__(self) -> None:
        self._nlp: Language = _load_spacy_model()

    # ── Public API ────────────────────────────────────────────────

    def process(self, text: str) -> ProcessedText:
        """
        Run the full preprocessing pipeline on `text`.

        Returns a `ProcessedText` dataclass with all extracted artefacts.
        Text is truncated to 100,000 characters to stay within spaCy limits.
        """
        if not text or not text.strip():
            return ProcessedText(raw=text or "", cleaned="")

        cleaned = self._clean(text)
        doc: Doc = self._nlp(cleaned[:100_000])

        return ProcessedText(
            raw=text,
            cleaned=cleaned,
            tokens=self._extract_tokens(doc),
            noun_chunks=self._extract_noun_chunks(doc),
            entities=[(ent.text, ent.label_) for ent in doc.ents],
            sentences=[sent.text.strip() for sent in doc.sents if sent.text.strip()],
        )

    def word_count(self, text: str) -> int:
        """Return approximate word count of `text`."""
        return len(text.split()) if text else 0

    def is_meaningful(self, text: str, min_words: int = 50) -> bool:
        """Return True if text has at least `min_words` words."""
        return self.word_count(text) >= min_words

    def get_candidate_phrases(self, text: str) -> list[str]:
        """
        Convenience method: return tokens + noun_chunks merged and
        deduplicated — used as candidate strings for the skill matcher.
        """
        result = self.process(text)
        seen: set[str] = set()
        phrases: list[str] = []
        for phrase in result.noun_chunks + result.tokens:
            phrase = phrase.lower().strip()
            if phrase and phrase not in seen:
                seen.add(phrase)
                phrases.append(phrase)
        return phrases

    # ── Private helpers ───────────────────────────────────────────

    def _clean(self, text: str) -> str:
        """Strip HTML-ish artefacts, bullets, and excessive whitespace."""
        text = self._URL_RE.sub(" ", text)
        text = self._EMAIL_RE.sub(" ", text)
        text = self._BULLET_RE.sub(" ", text)
        text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        text = self._WHITESPACE_RE.sub(" ", text)
        return text.strip()

    def _extract_tokens(self, doc: Doc) -> list[str]:
        """Lemmatise, lowercase, and filter stop words + punctuation."""
        tokens: list[str] = []
        for token in doc:
            if (
                not token.is_stop
                and not token.is_punct
                and not token.is_space
                and len(token.lemma_) > 1
                and token.lemma_.lower() not in _DOMAIN_STOP_WORDS
            ):
                tokens.append(token.lemma_.lower())
        return tokens

    def _extract_noun_chunks(self, doc: Doc) -> list[str]:
        """Extract multi-word noun phrases, cleaned and lowercased."""
        chunks: list[str] = []
        for chunk in doc.noun_chunks:
            text = chunk.text.lower().strip()
            # Remove leading determiners ('a python developer' → 'python developer')
            text = re.sub(r"^(a|an|the|our|your|their|its)\s+", "", text)
            text = self._PUNCT_RE.sub(" ", text).strip()
            text = self._WHITESPACE_RE.sub(" ", text)
            if text and len(text) > 2:
                chunks.append(text)
        return chunks
