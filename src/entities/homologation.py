from dataclasses import dataclass


@dataclass(frozen=True)
class SubjectMatch:
    source_subject: str
    target_subject: str
    score: float
    homologable: bool
    threshold: float
    evidence: list[str]


@dataclass(frozen=True)
class SubjectHomologationResult:
    source_subject: str
    best_match: SubjectMatch | None
    alternatives: list[SubjectMatch]


@dataclass(frozen=True)
class CareerHomologationReport:
    source_program: str
    target_program: str
    threshold: float
    total_source_subjects: int
    homologable_subjects: int
    general_percentage: float
    results: list[SubjectHomologationResult]
