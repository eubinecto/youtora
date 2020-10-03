from dataclasses import dataclass

from djongo import models


class Channel(models.Model):
    pass


class Track(models.Model):
    pass


class Caption(models.Model):
    pass


class Video(models.Model):
    pass


#
# @dataclass
# class Chapter(Data):
#     id: str
#     parent_id: str
#     start: float
#     duration: float
#     title: str
#     prev_id: str = None
#     next_id: str = None
#
#     # setter methods
#     def set_prev_id(self, prev_chap_id):
#         self.prev_id = prev_chap_id
#
#     def set_next_id(self, next_chap_id):
#         self.next_id = next_chap_id
#
#     def to_json(self):
#         pass
#
#     def __str__(self) -> str:
#         return self.title


class MLGlossRaw(models.Model):
    pass


@dataclass
class MLGlossDesc:
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


class MLGloss(models.Model):
    pass
