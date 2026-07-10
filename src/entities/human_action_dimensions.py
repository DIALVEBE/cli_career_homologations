from dataclasses import dataclass

@dataclass(frozen=True)
class HumanActionDimensions:
  comprehend: bool
  act: bool
  do: bool
  communicate: bool
  feel: bool
