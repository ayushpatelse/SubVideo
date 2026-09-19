from dataclasses import dataclass
from subtitles.parser import SubtitleBlock

@dataclass
class SubtitleTrack:
    name : str
    blocks : list[SubtitleBlock]
    offset_ms : int = 0