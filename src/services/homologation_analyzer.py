from __future__ import annotations

from entities import CareerHomologationReport, Subject, SubjectHomologationResult, SubjectMatch
from gateways import SubjectComparatorGateway

from .deterministic_subject_comparator import DeterministicSubjectComparator
from .subject_similarity import subject_similarity


def analyze_homologation(
    source_subjects: list[Subject],
    target_subjects: list[Subject],
    threshold: float = 0.40,
    alternatives_limit: int = 3,
    comparator: SubjectComparatorGateway | None = None,
    preselect_limit: int | None = None,
) -> CareerHomologationReport:
    comparator = comparator or DeterministicSubjectComparator()
    results = [
        _analyze_subject(source, target_subjects, threshold, alternatives_limit, comparator, preselect_limit)
        for source in source_subjects
    ]
    homologable_subjects = sum(
        result.best_match is not None and result.best_match.homologable
        for result in results
    )
    total_source_subjects = len(source_subjects)

    return CareerHomologationReport(
        source_program=_program_name(source_subjects),
        target_program=_program_name(target_subjects),
        threshold=threshold,
        total_source_subjects=total_source_subjects,
        homologable_subjects=homologable_subjects,
        general_percentage=round(
            homologable_subjects / total_source_subjects if total_source_subjects else 0.0,
            4,
        ),
        results=results,
    )


def _analyze_subject(
    source: Subject,
    target_subjects: list[Subject],
    threshold: float,
    alternatives_limit: int,
    comparator: SubjectComparatorGateway,
    preselect_limit: int | None,
) -> SubjectHomologationResult:
    matches = []
    for target in _candidate_targets(source, target_subjects, preselect_limit):
        matches.append(comparator.compare(source, target, threshold))

    matches.sort(key=lambda match: match.score, reverse=True)
    best_match = matches[0] if matches else None

    return SubjectHomologationResult(
        source_subject=source.name,
        best_match=best_match,
        alternatives=matches[1:alternatives_limit],
    )


def _program_name(subjects: list[Subject]) -> str:
    for subject in subjects:
        if subject.program:
            return subject.program
    return ""


def _candidate_targets(
    source: Subject,
    target_subjects: list[Subject],
    preselect_limit: int | None,
) -> list[Subject]:
    if preselect_limit is None or preselect_limit >= len(target_subjects):
        return target_subjects

    scored_targets = [
        (subject_similarity(source, target)[0], target)
        for target in target_subjects
    ]
    scored_targets.sort(key=lambda item: item[0], reverse=True)
    return [target for _, target in scored_targets[:preselect_limit]]
