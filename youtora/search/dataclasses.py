from dataclasses import dataclass
from typing import Optional, List

from youtora.refine.dataclasses import Track


# this is the object that we want to build
@dataclass
class SrchQuery:
    # get the value of this later
    idx_name: Optional[str] = None
    body: Optional[dict] = None  # the complete body to be used for..


@dataclass
class SrchRes:
    highlight: dict
    """highlighted result"""


@dataclass
class GeneralSrchRes(SrchRes):
    """
    represents the search result
    """
    tracks: List[Track]
    """previous, current, next track"""

    features: dict
    """remaining features"""

    def to_dict(self) -> dict:
        return {
            'tracks': [track.to_dict() for track in self.tracks],
            'highlight': self.highlight,
            'features': self.features
        }


@dataclass
class OpensubSrchRes(SrchRes):
    response: str
    contexts: List[str]

    def to_dict(self) -> dict:
        return {
            'response': self.response,
            'highlight': self.highlight,
            'contexts': self.contexts
        }
