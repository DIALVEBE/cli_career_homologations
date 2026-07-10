from dataclasses import dataclass

from .human_action_dimensions import HumanActionDimensions

@dataclass(frozen=True)
class Competency:
    learningResults: str
    humanActionDimensions: HumanActionDimensions
    didacticActivities: str
    time: str
    deliverables: str
    didacticResources: str
