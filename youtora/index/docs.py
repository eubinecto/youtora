from elasticsearch_dsl import (
    Document,
    InnerDoc,
    Double,
    Text,
    Keyword,
    Boolean,
    RankFeature,
    Nested)
from elasticsearch_dsl.connections import connections

from config.settings import ELASTICSEARCH_DSL

# create a default connection to the host
es_connection = connections.create_connection(hosts=ELASTICSEARCH_DSL['default']['hosts'])


class ChannelInnerDoc(InnerDoc):
    id = Keyword(required=True)
    subs = RankFeature()
    lang_code = Keyword()


class VideoInnerDoc(InnerDoc):
    id = Keyword(required=True)
    views = RankFeature()
    likes = RankFeature()
    dislikes = RankFeature()
    like_ratio = RankFeature()
    publish_date_int = RankFeature()
    category = Text()
    channel = Nested(ChannelInnerDoc)


class CaptionInnerDoc(InnerDoc):
    id = Keyword(required=True)
    is_auto = Boolean()
    lang_code = Keyword()
    video = Nested(VideoInnerDoc)


class GeneralDoc(Document):
    # define the fields here
    start = Double()
    duration = Double()
    content = Text()
    prev_id = Keyword()
    next_id = Keyword()
    context = Text()
    caption = Nested(CaptionInnerDoc)

    class Index:
        name = "general_doc"
        # using the default settings for now.

    def save(self, **kwargs):
        # do something before save here, if you wish
        return super().save(**kwargs)


# on import, create the mappings in elasticsearch
GeneralDoc.init()
