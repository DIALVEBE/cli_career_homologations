from dataclasses import dataclass

@dataclass(frozen=True)
class HumanActionDimensions:
  comprehend: bool
  act: bool
  do: bool
  communicate: bool
  feel: bool

  def __eq__(self, other) -> bool:
    if not isinstance(other, HumanActionDimensions):
      return NotImplemented

    attribs = vars(self)
    other_attribs = vars(other)

    return all([value == other_attribs[attrib] for attrib, value in attribs.items()])
