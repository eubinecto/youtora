from django.core.validators import URLValidator
from djongo import models


# ---  Raw models (YouTube) --- #
class ChannelRaw(models.Model):
    objects = models.Manager()
    _id = models.CharField(primary_key=True, max_length=100, verbose_name="channel_id")
    url = models.URLField(validators=[URLValidator], null=False)
    lang_code = models.CharField(max_length=10, null=False)
    main_html = models.TextField(null=False)
    uploads_html = models.TextField(null=False)

    def __str__(self) -> str:
        return str(self._id)

    @property
    def id(self):
        return self._id


class TracksRaw(models.Model):
    objects = models.Manager()
    _id = models.CharField(primary_key=True, max_length=100, verbose_name="caption_id|tracks_raw")
    caption_id = models.CharField(max_length=100, null=False)
    xml = models.TextField(null=False)

    @property
    def id(self):
        return self._id


class VideoRaw(models.Model):
    objects = models.Manager()
    _id = models.CharField(primary_key=True, max_length=100, verbose_name="video_id")
    # on looking up channel_raw, djongo will create a pymongo query for that
    channel_raw = models.ForeignKey(to=ChannelRaw, null=False, on_delete=models.CASCADE)
    video_info = models.JSONField(null=False)  # every info will be stored here
    # this collection includes the captions separately

    def __str__(self) -> str:
        return str(self._id)

    @property
    def id(self):
        return self._id


# --- parsed models (ml glossary)  --- #
class MLGlossDesc(models.Model):
    """
    embedded field for MLGloss
    """
    class Meta:
        abstract = True
    # have to parse this.
    desc_raw = models.CharField(name='desc_raw', null=False)
    pure_text = models.CharField(name='pure_text', null=False)
    topic_sent = models.CharField(max_length=500, name='topic_sent', null=False)

    def set_all(self, desc_raw, pure_text, topic_sent):
        self.desc_raw = desc_raw
        self.pure_text = pure_text
        self.topic_sent = topic_sent


class MLGloss(models.Model):
    """
    parsed MLGloss. the definition may vary
    """
    objects = models.Manager()
    _id = models.CharField(max_length=100, name='id', primary_key=True)
    word = models.CharField(max_length=100, name='word', null=False)
    ref = models.URLField(validators=[URLValidator], name='ref', null=False)
    category = models.CharField(max_length=100, name='category')
    desc = models.EmbeddedField(model_container=MLGlossDesc, null=False)

    def set_all(self, ml_gloss_id: str,
                word: str, ref: str,
                category: str, desc: MLGlossDesc):
        self._id = ml_gloss_id
        self.word = word
        self.ref = ref
        self.category = category
        self.desc = desc
# --- parsed models (idioms from Wiktionary) --- #
