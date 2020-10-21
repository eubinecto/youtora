from djongo import models
from django.core.validators import URLValidator


# --- parsed models (ml glossary)  --- #
class MLGlossDesc(models.Model):
    """
    embedded field for MLGloss
    """
    class Meta:
        abstract = True
    # have to parse this.
    desc_raw = models.CharField(blank=False, null=False)
    pure_text = models.CharField(blank=False, null=False)
    topic_sent = models.CharField(max_length=500, blank=False, null=False)


class MLGloss(models.Model):
    """
    parsed MLGloss. the definition may vary
    """
    objects = models.Manager()
    _id = models.CharField(max_length=100, primary_key=True)
    word = models.CharField(max_length=100, blank=False, null=False)
    ref = models.URLField(validators=[URLValidator], blank=False, null=False)
    category = models.CharField(max_length=100)
    desc = models.EmbeddedField(model_container=MLGlossDesc, blank=False, null=False)

    @property
    def id(self) -> str:
        return self._id


# --- parsed models (idioms from Wiktionary) --- #
class IdiomDef(models.Model):
    class Meta:
        abstract = True
    pure_text = models.TextField(blank=False, null=False)  # only contains the pure text
    # add raw text later, when you really need it
    # raw_text = models.TextField(blank=False, null=False)  # contains the hyperlink as well
    context = models.TextField(blank=False, null=False)  # e.g. (rail transport) , (slang). etc


class Idiom(models.Model):
    objects = models.Manager()
    _id = models.CharField(primary_key=True, max_length=100)  # same as idiom raw
    idiom = models.CharField(max_length=100, blank=False, null=False)  # same as idiom raw
    wiktionary_url = models.URLField(validators=[URLValidator], blank=False, null=False)  # same as idiom raw
    defs = models.ArrayField(model_container=IdiomDef, blank=False, null=False)  # a list of definitions

    @property
    def id(self) -> str:
        return self._id
