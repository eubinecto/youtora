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


class CaptionsRaw(models.Model):
    """
    all the captions found for the given video
    """
    _id = models.CharField(primary_key=True, max_length=100, verbose_name="video_id|captions_raw")
    video_id = models.CharField(max_length=100, null=False)
    manual_captions_info = models.JSONField(null=False)
    auto_captions_info = models.JSONField(null=False)

    class Meta:
        abstract = True

    @property
    def id(self):
        return self._id

    def to_dict(self) -> dict:
        """
        :return: a dictionary representation of this class
        """
        fields = self._meta.get_fields()
        dict_rep = dict()
        for field in fields:
            dict_rep[field.name] = self._meta.get_field(field.name)
        return dict_rep


class VideoRaw(models.Model):
    objects = models.Manager()
    _id = models.CharField(primary_key=True, max_length=100, verbose_name="video_id")
    # on looking up channel_raw, djongo will create a pymongo query for that
    channel_raw = models.ForeignKey(to=ChannelRaw, null=False, on_delete=models.CASCADE)
    video_info = models.JSONField(null=False)
    # this collection includes the captions separately
    _captions_raw = models.EmbeddedField(model_container=CaptionsRaw, null=False)

    def __str__(self) -> str:
        return str(self._id)

    @property
    def id(self):
        return self._id

    @property
    def captions_raw(self) -> CaptionsRaw:
        captions_raw = CaptionsRaw()
        for field_name, field_val in self._captions_raw.items():
            # https://medium.com/@mgarod/dynamically-add-a-method-to-a-class-in-python-c49204b85bd6
            setattr(captions_raw, field_name, field_val)
        return captions_raw

    @captions_raw.setter
    def captions_raw(self, captions_raw: CaptionsRaw):
        self._captions_raw = captions_raw.to_dict()


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
