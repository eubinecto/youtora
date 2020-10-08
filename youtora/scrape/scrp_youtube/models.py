
# from typing import List
from django.core.validators import URLValidator
from djongo import models
from .settings import LANG_CODES_TO_COLLECT


class Channel(models.Model):
    _id = models.ObjectIdField()
    url = models.URLField(validators=[URLValidator], name='url')
    title = models.CharField(max_length=100, name='title')
    subs = models.IntegerField(name='subs')
    lang_code = models.CharField(max_length=5, choices=LANG_CODES_TO_COLLECT)

    # # getter
    # @property
    # def vid_ids(self) -> List[str]:
    #     return self._vid_ids
    #
    # # setter
    # @vid_ids.setter
    # def vid_ids(self, vid_ids: List[str]):
    #     self._vid_ids = vid_ids

    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return str(self.title)


class Video(models.Model):
    _id = models.ObjectIdField()
    channel = models.ForeignKey(to=Channel, name='channel', on_delete=models.CASCADE)
    url = models.URLField(validators=[URLValidator], name='url')
    title = models.CharField(max_length=100, name='title')
    publish_date = models.DateField(name='publish_date')
    likes = models.IntegerField(name='likes')
    dislikes = models.IntegerField(name='dislikes')
    views = models.IntegerField(name='views')
    category = models.CharField(max_length=100, name='category')

    # @property
    # def manual_sub_info(self) -> dict:
    #     return self._manual_sub_info
    #
    # @property
    # def auto_sub_info(self) -> dict:
    #     return self._auto_sub_info
    #
    # @property
    # def captions(self) -> List[Caption]:
    #     return self._captions
    #
    # @manual_sub_info.setter
    # def manual_sub_info(self, manual_sub_info: dict):
    #     self._manual_sub_info = manual_sub_info
    #
    # @auto_sub_info.setter
    # def auto_sub_info(self, auto_sub_info: dict):
    #     self._auto_sub_info = auto_sub_info
    #
    # @captions.setter
    # def captions(self, captions: List[Caption]):
    #     self._captions: List[Caption] = captions

    # overrides the dunder string method
    def __str__(self) -> str:
        return str(self.title)


class Caption(models.Model):
    _id = models.ObjectIdField()
    video = models.ForeignKey(to=Video, name='video', on_delete=models.CASCADE)
    is_auto = models.BooleanField(name='is_auto')
    lang_code = models.CharField(max_length=10, choices=LANG_CODES_TO_COLLECT, name='lang_code')
    url = models.URLField(validators=[URLValidator], name='url')

    # # getter method
    # @property
    # def tracks(self) -> List[Track]:
    #     return self.tracks
    #
    # # setter method
    # @tracks.setter
    # def tracks(self, tracks: List[Track]):
    #     self.tracks: List[Track] = tracks

    # overrides dunder string method
    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return str("|".join([self._id, self.video, str(self.is_auto), self.lang_code]))


class Track(models.Model):
    _id = models.ObjectIdField()
    caption = models.ForeignKey(to=Caption, on_delete=models.CASCADE)
    # these three are nullable
    prev_track = models.OneToOneField(to='self',
                                      null=True,
                                      related_name="+",
                                      on_delete=models.CASCADE)
    next_track = models.OneToOneField(to='self',
                                      null=True,
                                      on_delete=models.CASCADE)
    context = models.CharField(max_length=100, null=True, name='context')
    start = models.FloatField(name='start')
    duration = models.FloatField(name='duration')
    content = models.CharField(max_length=100, name='content')

    # overrides dunder string method
    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return str(self.content)

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
