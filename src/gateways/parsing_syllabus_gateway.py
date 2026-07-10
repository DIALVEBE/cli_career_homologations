from typing import Protocol
from pathlib import Path

from entities import Subject

class ParsingSyllabusGateway(Protocol):
    """
    Source of syllabus information
    """
    def extract_subject_from_syllabus(path: Path) -> Subject:
        ...
