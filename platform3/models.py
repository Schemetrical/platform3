from dataclasses import dataclass
from enum import Enum

class LineID(str, Enum):
  G = "G"
  J = "J"
  L = "L"

@dataclass
class Train:
  line_id: LineID
  terminus: str
  eta: int

@dataclass
class Stop:
  line_id: LineID
  stop_id: str
  min_walking_distance: int = 0
