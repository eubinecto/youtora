from dataclasses import dataclass
from typing import List


# --- YouTube --- #
@dataclass
class Channel:
    """
    define the parsed version here.
    """
    id: str  # id must be the same as channel_id Raw.
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
class Track:
    caption_id: str
    start: float
    duration: float
    content: str
    # these are optionals
    prev_id: str = None
    next_id: str = None
    context: str = None
    timed_url: str = None

    @property
    def id(self) -> str:
        """
        combine with the hash value of the track to get the id.
        :return: the id of this track.
        """
        return "|".join([self.caption_id, str(self.__hash__())])

    def __hash__(self) -> int:
        return hash((self.caption_id, self.start, self.content))

    # overrides dunder string method
    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.content

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'caption_id': self.caption_id,
            'start': self.start,
            'duration': self.duration,
            'content': self.content,
            'context': self.context,
            'prev_id': self.prev_id,
            'next_id': self.next_id,
            'timed_url': self.timed_url
        }


@dataclass
class Caption:
    id: str
    video_id: str
    is_auto: bool
    lang_code: str
    url: str

    # overrides dunder string method
    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.id


@dataclass
class Video:
    id: str
    channel_id: str
    url: str
    title: str
    publish_date: str
    # likes: int
    # dislikes: int
    views: int
    category: str

    # manual_captions_info: dict
    # auto_captions_info: dict

    # overrides the dunder string method
    def __str__(self) -> str:
        return self.title
