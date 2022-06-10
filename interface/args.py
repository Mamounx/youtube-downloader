from dataclasses import dataclass
from typing import Optional

@dataclass
class Args:
    video: str = None
    playlist: str = None
    resolution: str = None