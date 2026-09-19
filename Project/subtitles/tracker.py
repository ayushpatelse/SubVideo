from dataclasses import dataclass
from parser import SubtitleBlock

@dataclass
class SubtitleTrack:
    blocks : list[SubtitleBlock]
    offset_ms : int = 0