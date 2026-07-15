from entities import Subject, SubjectMatch

from .subject_similarity import normalized_name_similarity, subject_similarity


class DeterministicSubjectComparator:
    def compare(self, source: Subject, target: Subject, threshold: float) -> SubjectMatch:
        credit_match = _credit_aware_name_match(source, target, threshold)
        if credit_match is not None:
            return credit_match

        score, evidence = subject_similarity(source, target)
        return SubjectMatch(
            source_subject=source.name,
            target_subject=target.name,
            score=score,
            homologable=score >= threshold,
            threshold=threshold,
            evidence=evidence,
            source_credits=source.credits,
            target_credits=target.credits,
        )


def _credit_aware_name_match(source: Subject, target: Subject, threshold: float) -> SubjectMatch | None:
    if _has_conflicting_level(source.name, target.name):
        return None

    name_score = normalized_name_similarity(source.name, target.name)
    if name_score < 0.95 or source.credits is None or target.credits is None:
        return None

    if source.credits >= target.credits:
        return SubjectMatch(
            source_subject=source.name,
            target_subject=target.name,
            score=1.0,
            homologable=True,
            threshold=threshold,
            evidence=[
                "Homologación directa por nombre equivalente.",
                f"Créditos suficientes: origen {source.credits}, destino {target.credits}.",
            ],
            source_credits=source.credits,
            target_credits=target.credits,
        )

    credit_ratio = round(source.credits / target.credits, 4)
    return SubjectMatch(
        source_subject=source.name,
        target_subject=target.name,
        score=credit_ratio,
        homologable=False,
        threshold=threshold,
        evidence=[
            "Nombre equivalente, pero no homologable por déficit de créditos.",
            f"Créditos insuficientes: origen {source.credits}, destino {target.credits}.",
        ],
        source_credits=source.credits,
        target_credits=target.credits,
    )


def _has_conflicting_level(source_name: str, target_name: str) -> bool:
    source_level = _course_level(source_name)
    target_level = _course_level(target_name)
    return source_level is not None and target_level is not None and source_level != target_level


def _course_level(name: str) -> str | None:
    tokens = name.replace("-", " ").split()
    if not tokens:
        return None

    last = tokens[-1].strip(" .()").upper()
    roman_levels = {"I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"}
    if last in roman_levels:
        return last
    if last.isdigit():
        return last
    return None
