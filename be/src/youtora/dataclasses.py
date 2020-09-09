from typing import List
from dataclasses import dataclass


class Data:
    def __init__(self):
        self.id = None


class YouTubeData(Data):
    def __init__(self):
        super().__init__()
        self.parent_id = None


@dataclass
class Channel(YouTubeData):
    id: str
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
class Track(YouTubeData):
    id: str
    parent_id: str
    start: float
    duration: float
    content: str
    # these are optionals
    prev_id: str = None
    next_id: str = None
    context: str = None

    def set_prev_id(self, prev_id: str):
        self.prev_id = prev_id

    def set_next_id(self, next_id: str):
        self.next_id = next_id

    def set_context(self, context: str):
        self.context: str = context

    # overrides dunder string method
    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.id


@dataclass
class Caption(YouTubeData):
    id: str
    parent_id: str
    is_auto: bool
    lang_code: str
    url: str
    tracks: List[Track] = None

    # setter method
    def set_tracks(self, tracks: List[Track]):
        self.tracks: List[Track] = tracks

    # overrides dunder string method
    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.id


@dataclass
class Video(YouTubeData):
    id: str
    parent_id: str
    url: str
    title: str
    publish_date: str
    likes: int
    dislikes: int
    views: int
    category: str
    manual_sub_info: dict
    auto_sub_info: dict
    captions: List[Caption] = None

    def set_captions(self, captions: List[Caption]):
        self.captions: List[Caption] = captions

    # overrides the dunder string method
    def __str__(self) -> str:
        return self.title


@dataclass
class Chapter(YouTubeData):
    id: str
    parent_id: str
    start: float
    duration: float
    title: str
    prev_id: str = None
    next_id: str = None

    # setter methods
    def set_prev_id(self, prev_chap_id):
        self.prev_id = prev_chap_id

    def set_next_id(self, next_chap_id):
        self.next_id = next_chap_id

    def __str__(self) -> str:
        return self.title


# class Frame(Data):
#
#     __slots__ = (
#         "id",
#         "parent_id",
#         "timestamp"
#     )
#
#     def __init__(self,
#                  frame_id: str,
#                  vid_id: str,
#                  timestamp: int):
#         """
#         :param frame_id:
#         :param vid_id:
#         :param timestamp: the should be an integer.
#         """
#
#         super().__init__()
#         self.id = frame_id
#         self.parent_id = vid_id
#         self.timestamp = timestamp

@dataclass
class MLGlossRaw(Data):
    id: str
    word: str
    credit: str
    desc_raw: str
    category_raw: str

    def to_json(self) -> dict:
        doc = {
                '_id': self.id,
                'word': self.word,
                "credit": self.credit,
                "desc_raw": self.desc_raw,
                "category_raw": self.category_raw
        }
        return doc

    def __str__(self) -> str:
        return self.word


@dataclass
class MLGlossDesc(Data):
    topic_sent: str
    pure_text: str
    desc_raw: str

    def to_json(self) -> dict:
        doc = {
            "topic_sent": self.topic_sent,
            "pure_text": self.pure_text,
            "desc_raw": self.desc_raw
        }
        return doc


@dataclass
class MLGloss(Data):
    id: str
    word: str
    credit: str
    desc: MLGlossDesc
    category: str

    def to_json(self) -> dict:
        doc = {
            "_id": self.id,
            "credit": self.credit,
            "word": self.word,
            "desc": self.desc.to_json(),
            "category": self.category
        }
        return doc
