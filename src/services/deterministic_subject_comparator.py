from entities import Subject, SubjectMatch

from .subject_similarity import subject_similarity


class DeterministicSubjectComparator:
    def compare(self, source: Subject, target: Subject, threshold: float) -> SubjectMatch:
        score, evidence = subject_similarity(source, target)
        return SubjectMatch(
            source_subject=source.name,
            target_subject=target.name,
            score=score,
            homologable=score >= threshold,
            threshold=threshold,
            evidence=evidence,
        )
