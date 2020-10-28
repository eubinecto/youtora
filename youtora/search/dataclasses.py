from dataclasses import dataclass
from typing import Optional, List

from youtora.refine.dataclasses import Track


@dataclass
class SrchQuery:
    text: str
    """the text to match with"""
    is_auto: Optional[bool] = None
    """auto / manual constraint for captions"""
    capt_lang_code: Optional[str] = None
    """lang_code constraint for captions"""
    chan_lang_code: Optional[str] = None
    """lang_code constraint for channel"""
    views_boost: int = 10
    subs_boost: int = 10
    from_: int = 0
    size: int = 10


@dataclass
class SrchResult:
    """
    represents the search result
    """
    tracks: List[Track]
    """previous, current, next track"""
    highlight: str
    """highlighted result"""
    features: dict
    """remaining features"""

    def to_dict(self) -> dict:
        return {
            'tracks': [track.to_dict() for track in self.tracks],
            'highlight': self.highlight,
            'features': self.features
        }
