from django.core.validators import URLValidator
from djongo import models


# ---  Raw models (YouTube) --- #
class ChannelRaw(models.Model):
    objects = models.Manager()
    id = models.CharField(primary_key=True, max_length=100, verbose_name="channel_id")
    url = models.URLField(validators=[URLValidator])
    lang_code = models.CharField(max_length=10)
    main_html = models.TextField()
    uploads_html = models.TextField()


class TracksRaw(models.Model):
    objects = models.Manager()
    id = models.CharField(primary_key=True, max_length=100, verbose_name="caption_id|tracks")
    caption_id = models.CharField(max_length=100)
    xml = models.TextField()


class CaptionsRaw(models.Model):
    """
    all the captions found for the given video
    """
    id = models.CharField(primary_key=True, max_length=100, verbose_name="video_id|captions")
    video_id = models.CharField(max_length=100)
    manual_captions_json = models.TextField()
    auto_captions_json = models.TextField()

    class Meta:
        abstract = True


class VideoRaw(models.Model):
    objects = models.Manager()
    id = models.CharField(primary_key=True, max_length=100, verbose_name="video_id")
    channel_id = models.CharField(max_length=100)
    video_info_json = models.TextField()
    # this collection includes the captions separately
    captions_raw = models.EmbeddedField(model_container=CaptionsRaw)


# --- parsed models (ml glossary)  --- #

class MLGlossDesc(models.Model):
    """
    embedded field for MLGloss
    """
    class Meta:
        abstract = True
    # have to parse this.
    desc_raw = models.CharField(name='desc_raw')
    pure_text = models.CharField(name='pure_text')
    topic_sent = models.CharField(max_length=500, name='topic_sent')

    def set_all(self, desc_raw, pure_text, topic_sent):
        self.desc_raw = desc_raw
        self.pure_text = pure_text
        self.topic_sent = topic_sent


class MLGloss(models.Model):
    """
    parsed MLGloss. the definition may vary
    """
    objects = models.Manager()
    id = models.CharField(max_length=100, name='id', primary_key=True)
    word = models.CharField(max_length=100, name='word')
    ref = models.URLField(validators=[URLValidator], name='credit')
    category = models.CharField(max_length=100, name='category')
    desc = models.EmbeddedField(model_container=MLGlossDesc)

    def set_all(self, ml_gloss_id: str,
                word: str, ref: str,
                category: str, desc: MLGlossDesc):
        self.id = ml_gloss_id
        self.word = word
        self.ref = ref
        self.category = category
        self.desc = desc
# --- parsed models (idioms from Wiktionary) --- #
