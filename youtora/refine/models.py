from django.contrib.postgres.fields import JSONField, ArrayField
from django.core.validators import URLValidator
from django.db import models


# # --- parsed models (ml glossary)  --- #
# class MLGlossDesc(models.Model):
#     """
#     embedded field for MLGloss
#     """
#     class Meta:
#         abstract = True
#     # have to parse this.
#     desc_raw = models.CharField(blank=False, null=False)
#     text = models.CharField(blank=False, null=False)
#     topic_sent = models.CharField(max_length=500, blank=False, null=False)
#
#
# class MLGloss(models.Model):
#     """
#     parsed MLGloss. the definition may vary
#     """
#     objects = models.Manager()
#     id = models.CharField(max_length=100, primary_key=True)
#     word = models.CharField(max_length=100, blank=False, null=False)
#     ref = models.URLField(validators=[URLValidator], blank=False, null=False)
#     category = models.CharField(max_length=100)
#     desc = models.EmbeddedField(model_container=MLGlossDesc, blank=False, null=False)
#
#     @property
#     def id(self) -> str:
#         return self.id


# --- parsed models (idioms from Wiktionary) --- #
class Idiom(models.Model):
    objects = models.Manager()
    id = models.CharField(primary_key=True, max_length=100)  # same as text raw
    text = models.CharField(max_length=100, blank=False, null=False)  # same as text raw
    wiktionary_url = models.URLField(validators=[URLValidator], blank=False, null=False)  # same as text raw
    # a list of definition sets.
    meanings = ArrayField(base_field=JSONField(blank=True, null=False),
                          blank=True, null=False, default=list)

    def __str__(self) -> str:
        return str(self.text)

    def save(self, **kwargs):
        # note: always do model.clean_fields() before model.save()
        # https://stackoverflow.com/questions/17816229/django-model-blank-false-does-not-work
        self.clean_fields()
        # self.validate_unique()
        super(Idiom, self).save()
