
from typing import List
from django.core.validators import URLValidator
from djongo import models

# temporarily placed here
LANG_CODES_TO_COLLECT = ('ko', 'ja', 'en', 'en-GB', 'fr')


class Channel(models.Model):
    global LANG_CODES_TO_COLLECT
    id = models.CharField(max_length=100, name='id')
    url = models.URLField(validators=[URLValidator], name='url')
    title = models.CharField(max_length=100, name='title')
    subs = models.IntegerField(name='subs')
    lang_code = models.CharField(max_length=5, choices=LANG_CODES_TO_COLLECT)

    # getter
    @property
    def vid_ids(self) -> List[str]:
        return self._vid_ids

    # setter
    @vid_ids.setter
    def vid_ids(self, vid_ids: List[str]):
        self._vid_ids = vid_ids

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
        return str(self.title)


class Track(models.Model):
    parent_id = models.CharField(max_length=100, name='parent_id')
    # these three are nullable
    prev_id = models.CharField(max_length=100, null=True, name='prev_id')
    next_id = models.CharField(max_length=100, null=True, name='next_id')
    context = models.CharField(max_length=100, null=True, name='context')
    start = models.FloatField(name='start')
    duration = models.FloatField(name='duration')
    content = models.CharField(max_length=100, name='content')

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
        return str(self.content)


class Caption(models.Model):
    global LANG_CODES_TO_COLLECT
    id = models.CharField(max_length=100, name='id')
    parent_id = models.CharField(max_length=100, name='parent_id')
    is_auto = models.BooleanField(name='is_auto')
    lang_code = models.CharField(choices=LANG_CODES_TO_COLLECT, name='lang_code')
    url = models.URLField(validators=[URLValidator], name='url')

    # getter method
    @property
    def tracks(self) -> List[Track]:
        return self.tracks

    # setter method
    @tracks.setter
    def tracks(self, tracks: List[Track]):
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
        return str(self.id)


caption = Caption()


class Video(models.Model):
    id = models.CharField(max_length=100, name='id')
    parent_id = models.CharField(max_length=100, name='parent_id')
    url = models.URLField(validators=[URLValidator], name='url')
    title = models.CharField(max_length=100, name='title')
    publish_date = models.DateField(name='publish_date')
    likes = models.IntegerField(name='likes')
    dislikes = models.IntegerField(name='dislikes')
    views = models.IntegerField(name='views')
    category = models.CharField(max_length=100, name='category')

    @property
    def manual_sub_info(self) -> dict:
        return self.manual_sub_info

    @property
    def auto_sub_info(self) -> dict:
        return self.auto_sub_info

    @property
    def captions(self) -> List[Caption]:
        return self.captions

    @manual_sub_info.setter
    def manual_sub_info(self, manual_sub_info: dict):
        self.manual_sub_info = manual_sub_info

    @auto_sub_info.setter
    def auto_sub_info(self, auto_sub_info: dict):
        self.auto_sub_info = auto_sub_info

    @captions.setter
    def captions(self, captions: List[Caption]):
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
            "category": self.category
        }  # doc

    # overrides the dunder string method
    def __str__(self) -> str:
        return str(self.title)


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
    id = models.CharField(max_length=100, name='id')
    word = models.CharField(max_length=100, name='word')
    credit = models.CharField(max_length=100, name='credit')
    desc_raw = models.CharField(max_length=100, name='desc_raw')
    category_raw = models.CharField(max_length=100, name='category_raw')

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
        return str(self.word)


class MLGlossDesc(models.Model):
    topic_sent = models.CharField(max_length=500, name='topic_sent')
    pure_text = models.CharField(name='pure_text')
    desc_raw = models.CharField(name='desc_raw')

    def to_json(self) -> dict:
        doc = {
            "topic_sent": self.topic_sent,
            "pure_text": self.pure_text,
            "desc_raw": self.desc_raw
        }
        return doc


class MLGloss(models.Model):
    id = models.CharField(max_length=100, name='id')
    word = models.CharField(max_length=100, name='word')
    credit = models.URLField(validators=[URLValidator], name='credit')
    category = models.CharField(max_length=100, name='category')
    desc = models.EmbeddedField(model_container=MLGlossDesc)
