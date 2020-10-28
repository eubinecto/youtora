from django.core.validators import URLValidator
from djongo import models


# ---  Raw models (YouTube) --- #
class ChannelRaw(models.Model):
    objects = models.Manager()
    _id = models.CharField(primary_key=True, max_length=100)
    url = models.URLField(validators=[URLValidator], blank=False)
    lang_code = models.CharField(max_length=10, blank=False)
    main_html = models.TextField(blank=False)
    uploads_html = models.TextField(blank=False)

    def __str__(self) -> str:
        return str(self.id)

    def save(self, **kwargs):
        # note: always do model.clean_fields() before model.save()
        # https://stackoverflow.com/questions/17816229/django-model-blank-false-does-not-work
        self.clean_fields()
        self.validate_unique()
        super(ChannelRaw, self).save()

    @property
    def id(self) -> str:
        return self._id


class VideoRaw(models.Model):
    objects = models.Manager()
    _id = models.CharField(primary_key=True, max_length=100)
    # on looking up channel_id, djongo will create a pymongo query for that
    url = models.URLField(validators=[URLValidator], blank=False)
    video_info = models.JSONField(blank=False, default=None)  # should be serialised with json.dumps
    main_html = models.TextField(blank=False)
    channel_id = models.CharField(max_length=100, blank=False)

    def __str__(self) -> str:
        return str(self.id)

    def save(self, **kwargs):
        # note: always do model.clean_fields() before model.save()
        # https://stackoverflow.com/questions/17816229/django-model-blank-false-does-not-work
        self.clean_fields()
        self.validate_unique()
        super(VideoRaw, self).save()

    @property
    def id(self) -> str:
        return self._id


class TracksRaw(models.Model):
    objects = models.Manager()
    _id = models.CharField(primary_key=True, max_length=100)
    # caption id must be unique
    caption_id = models.CharField(max_length=100, blank=False, unique=True)
    # can be null
    raw_xml = models.TextField(blank=True, default=None)

    # don't need a relation to video, as we'll look this up by caption id.

    def __str__(self) -> str:
        return str(self.id)

    def save(self, **kwargs):
        # note: always do model.clean_fields() before model.save()
        # https://stackoverflow.com/questions/17816229/django-model-blank-false-does-not-work
        self.clean_fields()
        self.validate_unique()  # must do this before saving
        super(TracksRaw, self).save()

    @property
    def id(self) -> str:
        return self._id


class IdiomRaw(models.Model):
    objects = models.Manager()
    _id = models.CharField(primary_key=True, max_length=100)
    text = models.CharField(max_length=100, blank=False)
    wiktionary_url = models.CharField(max_length=100, blank=False)
    # could be null
    parser_info = models.JSONField(blank=True, default=None)  # get this from wiktionary parser (python)
    # could be null (if request was erroneous)
    main_html = models.TextField(blank=True, default=None)

    def __str__(self) -> str:
        return self.text

    def save(self, **kwargs):
        # note: always do model.clean_fields() before model.save()
        # https://stackoverflow.com/questions/17816229/django-model-blank-false-does-not-work
        self.clean_fields()
        # self.validate_unique()  # must do this before saving
        super(IdiomRaw, self).save()

    @property
    def id(self) -> str:
        return self._id
