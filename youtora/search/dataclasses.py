from dataclasses import dataclass


@dataclass
class SearchQuery:
    text: str
    """the text to match with"""
    is_auto: bool
    """auto / manual constraint for captions"""
    capt_lang_code: str = None
    """lang_code constraint for captions"""
    chan_lang_code: str = None
    """lang_code constraint for channel"""
    views_boost: int = 10
    subs_boost: int = 10
    from_: int = 0
    size: int = 10
