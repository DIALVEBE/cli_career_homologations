from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

from entities import Subject

COURSE_PATTERN = re.compile(
    r"•\s*(?P<name>.+?)\s*\|\s*"
    r"(?:(?:Presencial|Virtual|Híbrida|Hibrida)\s*\|\s*)?"
    r"(?P<credits>\d+)\s*c",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class AcademicPlanCourse:
    name: str
    credits: int


def extract_academic_plan_courses(path: Path) -> list[AcademicPlanCourse]:
    return parse_academic_plan_text(_extract_pdf_text(path))


def academic_plan_subjects(path: Path, program: str | None = None) -> list[Subject]:
    program_name = program or _program_name_from_path(path)
    return [
        Subject(
            name=course.name,
            program=program_name,
            objective=course.name,
            problemicCore="",
            didacticStrategies="",
            competencies=[],
            credits=course.credits,
        )
        for course in extract_academic_plan_courses(path)
    ]


def parse_academic_plan_text(text: str) -> list[AcademicPlanCourse]:
    courses: list[AcademicPlanCourse] = []
    seen: set[str] = set()
    normalized_text = text.replace("\x00", " ")

    for match in COURSE_PATTERN.finditer(normalized_text):
        name = _clean_course_name(match.group("name"))
        credits = int(match.group("credits"))
        key = f"{_normalize_key(name)}:{credits}"
        if not name or key in seen:
            continue
        courses.append(AcademicPlanCourse(name=name, credits=credits))
        seen.add(key)

    return courses


def _extract_pdf_text(path: Path) -> str:
    reader = PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _clean_course_name(value: str) -> str:
    return " ".join(value.replace("\x00", " ").split()).strip(" .")


def _normalize_key(value: str) -> str:
    return " ".join(value.lower().split())


def _program_name_from_path(path: Path) -> str:
    return path.parent.name
