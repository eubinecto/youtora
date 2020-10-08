# using mongoDB as the backend
from djongo import models
from django.core.validators import URLValidator


class MLGlossRaw(models.Model):
    """
    MLGloss in Raw form
    """
    id = models.CharField(max_length=100, name='id', primary_key=True)
    word = models.CharField(max_length=100, name='word')
    credit = models.CharField(max_length=100, name='credit')
    desc_raw = models.CharField(max_length=100, name='desc_raw')
    category_raw = models.CharField(max_length=100, name='category_raw')

    def __str__(self) -> str:
        return str(self.word)


class MLGlossDesc(models.Model):
    """
    embedded field for MLGloss
    """
    class Meta:
        abstract = True
    topic_sent = models.CharField(max_length=500, name='topic_sent')
    pure_text = models.CharField(name='pure_text')
    desc_raw = models.CharField(name='desc_raw')


class MLGloss(models.Model):
    id = models.CharField(max_length=100, name='id', primary_key=True)
    word = models.CharField(max_length=100, name='word')
    credit = models.URLField(validators=[URLValidator], name='credit')
    category = models.CharField(max_length=100, name='category')
    desc = models.EmbeddedField(model_container=MLGlossDesc)