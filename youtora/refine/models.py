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
    desc_raw = models.CharField(name='desc_raw', blank=False, null=False)
    pure_text = models.CharField(name='pure_text', blank=False, null=False)
    topic_sent = models.CharField(max_length=500, blank=False, name='topic_sent', null=False)


class MLGloss(models.Model):
    """
    parsed MLGloss. the definition may vary
    """
    objects = models.Manager()
    _id = models.CharField(max_length=100, name='id', primary_key=True)
    word = models.CharField(max_length=100, name='word', blank=False, null=False)
    ref = models.URLField(validators=[URLValidator], name='ref', blank=False, null=False)
    category = models.CharField(max_length=100, name='category')
    desc = models.EmbeddedField(model_container=MLGlossDesc, blank=False, null=False)


# --- parsed models (idioms from Wiktionary) --- #
class IdiomDef(models.Model):
    class Meta:
        abstract = True
    def_text = models.TextField(blank=False, null=False)  # only contains the pure text
    def_raw = models.TextField(blank=False, null=False)  # contains the hyperlink as well
    context = models.TextField(blank=False, null=False)  # e.g. (rail transport) , (slang). etc


class Idiom(models.Model):
    objects = models.Manager()
    _id = models.CharField(primary_key=True, max_length=100, name='id')  # same as idiom raw
    idiom = models.CharField(max_length=100, blank=False, null=False)  # same as idiom raw
    wiktionary_url = models.URLField(validators=[URLValidator], blank=False, null=False)  # same as idiom raw
    defs = models.ArrayField(model_container=IdiomDef, blank=False, null=False)  # a list of definitions
