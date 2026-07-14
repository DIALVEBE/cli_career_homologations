from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher

from entities import Subject

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
STOPWORDS = {
    "a",
    "al",
    "and",
    "con",
    "de",
    "del",
    "el",
    "en",
    "for",
    "la",
    "las",
    "los",
    "of",
    "para",
    "por",
    "the",
    "to",
    "un",
    "una",
    "y",
}


def subject_similarity(source: Subject, target: Subject) -> tuple[float, list[str]]:
    name_score = _text_similarity(source.name, target.name)
    objective_score = _text_similarity(source.objective, target.objective)
    competency_score = _text_similarity(_competency_text(source), _competency_text(target))
    contents_score = _text_similarity(_contents_text(source), _contents_text(target))

    score = (
        name_score * 0.20
        + objective_score * 0.25
        + competency_score * 0.30
        + contents_score * 0.25
    )
    score = _apply_name_floor(score, name_score)

    evidence = [
        f"Nombre: {name_score:.0%}",
        f"Objetivo: {objective_score:.0%}",
        f"Competencias/resultados: {competency_score:.0%}",
        f"Contenidos: {contents_score:.0%}",
    ]
    return round(score, 4), evidence


def _apply_name_floor(score: float, name_score: float) -> float:
    if name_score >= 0.95:
        return max(score, 0.55)
    if name_score >= 0.75:
        return max(score, 0.42)
    return score


def _text_similarity(left: str, right: str) -> float:
    left_normalized = _normalize(left)
    right_normalized = _normalize(right)
    if not left_normalized or not right_normalized:
        return 0.0

    left_tokens = set(_tokens(left_normalized))
    right_tokens = set(_tokens(right_normalized))
    if not left_tokens or not right_tokens:
        return 0.0

    intersection = len(left_tokens & right_tokens)
    union = len(left_tokens | right_tokens)
    jaccard = intersection / union
    sequence = _sequence_similarity(left_normalized, right_normalized)

    return max(jaccard, sequence * 0.65)


def _sequence_similarity(left: str, right: str) -> float:
    max_length = 1200
    if len(left) > max_length or len(right) > max_length:
        return 0.0
    return SequenceMatcher(None, left, right).ratio()


def _tokens(value: str) -> list[str]:
    return [token for token in TOKEN_PATTERN.findall(value) if token not in STOPWORDS and len(token) > 2]


def _normalize(value: str) -> str:
    without_accents = unicodedata.normalize("NFKD", value.lower())
    ascii_value = "".join(char for char in without_accents if not unicodedata.combining(char))
    return " ".join(ascii_value.split())


def _competency_text(subject: Subject) -> str:
    chunks: list[str] = []
    for competency in subject.competencies:
        chunks.append(competency.name)
        chunks.extend(competency.learningResults)
    return " ".join(chunks)


def _contents_text(subject: Subject) -> str:
    return " ".join(competency.contents for competency in subject.competencies)
