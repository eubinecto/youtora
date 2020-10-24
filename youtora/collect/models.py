from django.contrib.postgres.fields import JSONField  # postgres - specific field
from django.core.validators import URLValidator
from django.db import models


# ---  Raw models (YouTube) --- #
class ChannelRaw(models.Model):
    objects = models.Manager()
    id = models.CharField(primary_key=True, max_length=100, verbose_name="channel_id")
    url = models.URLField(validators=[URLValidator], blank=False, null=False)
    lang_code = models.CharField(max_length=10, blank=False, null=False)
    main_html = models.TextField(blank=False, null=False)
    uploads_html = models.TextField(blank=False, null=False)

    def __str__(self) -> str:
        return str(self.id)

    def save(self, **kwargs):
        # note: always do model.clean_fields() before model.save()
        # https://stackoverflow.com/questions/17816229/django-model-blank-false-does-not-work
        self.clean_fields()
        # self.validate_unique()
        super(ChannelRaw, self).save()


class VideoRaw(models.Model):
    objects = models.Manager()
    id = models.CharField(primary_key=True, max_length=100, verbose_name="video_id")
    # on looking up channel_id, djongo will create a pymongo query for that
    url = models.URLField(validators=[URLValidator], blank=False, null=False)
    video_info = JSONField(blank=False, null=False)  # should be serialised with json.dumps
    main_html = models.TextField(blank=False, null=False)
    channel_id = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self) -> str:
        return str(self.id)

    def save(self, **kwargs):
        # note: always do model.clean_fields() before model.save()
        # https://stackoverflow.com/questions/17816229/django-model-blank-false-does-not-work
        self.clean_fields()
        self.validate_unique()
        super(VideoRaw, self).save()


class TracksRaw(models.Model):
    objects = models.Manager()
    id = models.CharField(primary_key=True, max_length=100, verbose_name="caption_id|tracks_raw")
    # caption id must be unique
    caption_id = models.CharField(max_length=100, blank=False, null=False, unique=True)
    # can be null
    raw_xml = models.TextField(blank=True, null=True, default=None)

    # don't need a relation to video, as we'll look this up by caption id.

    def __str__(self) -> str:
        return str(self.id)

    def save(self, **kwargs):
        # note: always do model.clean_fields() before model.save()
        # https://stackoverflow.com/questions/17816229/django-model-blank-false-does-not-work
        self.clean_fields()
        self.validate_unique()  # must do this before saving
        super(TracksRaw, self).save()


class IdiomRaw(models.Model):
    objects = models.Manager()
    id = models.CharField(primary_key=True, max_length=100)
    text = models.CharField(max_length=100, blank=False, null=False)
    wiktionary_url = models.CharField(max_length=100, blank=False, null=False)
    # could be null
    parser_info = JSONField(blank=True, null=True)  # get this from wiktionary parser (python)
    # could be null (if request was erroneous)
    main_html = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.text

    def save(self, **kwargs):
        # note: always do model.clean_fields() before model.save()
        # https://stackoverflow.com/questions/17816229/django-model-blank-false-does-not-work
        self.clean_fields()
        self.validate_unique()  # must do this before saving
        super(IdiomRaw, self).save()
