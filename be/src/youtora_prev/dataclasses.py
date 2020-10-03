from typing import List
from dataclasses import dataclass


@dataclass
class Data:

    def to_json(self) -> dict:
        raise NotImplementedError


@dataclass
class Channel(Data):
    id: str
    url: str
    title: str
    subs: int
    lang_code: str
    vid_id_list: List[str]

    def to_json(self) -> dict:
        return {
            "_id": self.id,
            "url": self.url,
            "title": self.title,
            "subs": self.subs,
            "lang_code": self.lang_code
        }

    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.title


@dataclass
class Track(Data):
    parent_id: str
    start: float
    duration: float
    content: str
    # these are optionals
    prev_id: str = None
    next_id: str = None
    context: str = None

    def get_id(self) -> str:
        """
        combine with the hash value of the track to get the id.
        :return: the id of this track.
        """
        return "|".join([self.parent_id, str(self.__hash__())])

    def set_prev_id(self, prev_id: str):
        self.prev_id = prev_id

    def set_next_id(self, next_id: str):
        self.next_id = next_id

    def set_context(self, context: str):
        self.context: str = context

    def to_json(self) -> dict:
        return {
            "_id": self.get_id(),
            "parent_id": self.parent_id,
            "start": self.start,
            "duration": self.duration,
            "content": self.content,
            "prev_id": self.prev_id,
            "next_id": self.next_id,
            "context": self.context
        }

    def __hash__(self) -> int:
        return hash((self.parent_id, self.start, self.content))

    # overrides dunder string method
    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.content


@dataclass
class Caption(Data):
    id: str
    parent_id: str
    is_auto: bool
    lang_code: str
    url: str
    tracks: List[Track] = None

    # setter method
    def set_tracks(self, tracks: List[Track]):
        self.tracks: List[Track] = tracks

    def to_json(self) -> dict:
        return {
            # video is the parent of caption
            "_id": self.id,
            "parent_id": self.parent_id,
            "url": self.url,
            "lang_code": self.lang_code,
            "is_auto": self.is_auto
        }

    # overrides dunder string method
    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.id


@dataclass
class Video(Data):
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

    def to_json(self) -> dict:
        return {
            # should add this field
            "_id": self.id,
            "parent_id": self.parent_id,
            "url": self.url,
            "title": self.title,
            "publish_date": self.publish_date,
            "views": self.views,
            "likes": self.likes,
            "dislikes": self.dislikes,
            "category_raw": self.category
        }  # doc

    # overrides the dunder string method
    def __str__(self) -> str:
        return self.title


@dataclass
class Chapter(Data):
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

    def to_json(self):
        pass

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
