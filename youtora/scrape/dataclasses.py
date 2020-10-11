from typing import List
from dataclasses import dataclass


# --- YouTube --- #
@dataclass
class ChannelData:
    """
    define the parsed version here.
    """
    id: str  # id must be the same as channel Raw.
    url: str
    title: str
    subs: int
    lang_code: str
    vid_id_list: List[str]

    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.title


@dataclass
class TrackData:
    caption_id: str
    start: float
    duration: float
    content: str
    # these are optionals
    prev_id: str = None
    next_id: str = None
    context: str = None

    @property
    def id(self) -> str:
        """
        combine with the hash value of the track to get the id.
        :return: the id of this track.
        """
        return "|".join([self.caption_id, str(self.__hash__())])

    def set_prev_id(self, prev_id: str):
        self.prev_id = prev_id

    def set_next_id(self, next_id: str):
        self.next_id = next_id

    def set_context(self, context: str):
        self.context: str = context

    def __hash__(self) -> int:
        return hash((self.caption_id, self.start, self.content))

    # overrides dunder string method
    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.content


@dataclass
class CaptionData:
    id: str
    video_id: str
    is_auto: bool
    lang_code: str
    url: str
    tracks: List[TrackData] = None

    # setter method
    def set_tracks(self, tracks: List[TrackData]):
        self.tracks: List[TrackData] = tracks

    # overrides dunder string method
    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.id


@dataclass
class VideoData:
    id: str
    channel_id: str
    url: str
    title: str
    publish_date: str
    likes: int
    dislikes: int
    views: int
    category: str
    manual_captions_info: dict
    auto_captions_info: dict
    captions: List[CaptionData] = None

    def set_captions(self, captions: List[CaptionData]):
        self.captions: List[CaptionData] = captions

    # overrides the dunder string method
    def __str__(self) -> str:
        return self.title
