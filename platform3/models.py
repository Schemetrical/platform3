from dataclasses import dataclass

@dataclass
class Train:
  line_id: str
  terminus: str
  eta: int

@dataclass
class Stop:
  line_id: str
  stop_id: str
  min_walking_distance: int = 0
