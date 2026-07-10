from dataclasses import dataclass

from .competency import Competency

@dataclass(frozen=True)
class Subject:
    name: str
    program: str
    objective: str
    didacticStrategies: str
    competencies: list[Competency]
