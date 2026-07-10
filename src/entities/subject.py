from dataclasses import dataclass

from .competency import Competency

@dataclass(frozen=True)
class Subject:
    name: str
    program: str
    objective: str
    problemicCore: str
    didacticStrategies: str
    competencies: list[Competency]
