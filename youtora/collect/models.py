from django.core.validators import URLValidator
from djongo import models


# ---  Raw models (YouTube) --- #
class ChannelRaw(models.Model):
    objects = models.Manager()
    _id = models.CharField(primary_key=True, max_length=100, verbose_name="channel_id")
    url = models.URLField(validators=[URLValidator], blank=False, null=False)
    lang_code = models.CharField(max_length=10, blank=False, null=False)
    main_html = models.TextField(blank=False, null=False)
    uploads_html = models.TextField(blank=False, null=False)

    def __str__(self) -> str:
        return str(self._id)

    @property
    def id(self):
        return self._id


class TracksRaw(models.Model):
    objects = models.Manager()
    _id = models.CharField(primary_key=True, max_length=100, verbose_name="caption_id|tracks_raw")
    caption_id = models.CharField(max_length=100, blank=False, null=False)
    raw_xml = models.TextField(blank=False, null=False)

    @property
    def id(self):
        return self._id


class VideoRaw(models.Model):
    objects = models.Manager()
    _id = models.CharField(primary_key=True, max_length=100, verbose_name="video_id")
    # on looking up channel_id, djongo will create a pymongo query for that
    url = models.URLField(validators=[URLValidator], blank=False, null=False)
    channel_id = models.CharField(max_length=100, blank=False, null=False)
    video_info = models.JSONField(blank=False, null=False)  # every info will be stored here
    main_html = models.TextField(blank=False, null=False)
    # this collection includes the captions separately

    def __str__(self) -> str:
        return str(self._id)

    @property
    def id(self):
        return self._id

