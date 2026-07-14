from typing import Protocol

from entities import Subject, SubjectMatch


class SubjectComparatorGateway(Protocol):
    def compare(self, source: Subject, target: Subject, threshold: float) -> SubjectMatch:
        ...
