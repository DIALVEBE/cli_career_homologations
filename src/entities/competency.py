from dataclasses import dataclass

from .human_action_dimensions import HumanActionDimensions

@dataclass(frozen=True)
class Competency:
    name: str
    humanActionDimensions: HumanActionDimensions
    learningResults: list[str]
    contents: str
    time: str
    evaluationMechanisms: str
    didacticResources: str
