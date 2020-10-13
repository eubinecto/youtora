from elasticsearch_dsl.connections import connections
from config.settings import ELASTICSEARCH_DSL
from elasticsearch_dsl import (
     Document,
     InnerDoc,
     Double,
     Text,
     Keyword,
     Boolean,
     RankFeature,
     Nested)


# create a default connection to the host
connections.create_connection(hosts=ELASTICSEARCH_DSL['default']['hosts'])


class ChannelInnerDoc(InnerDoc):
    id = Keyword()
    subs = RankFeature()
    lang_code = Keyword()


class VideoInnerDoc(InnerDoc):
    id = Keyword()
    views = RankFeature()
    likes = RankFeature()
    dislikes = RankFeature()
    like_ratio = RankFeature()
    publish_date_int = RankFeature()
    category = Text()
    channel = Nested(ChannelInnerDoc)


class CaptionInnerDoc(InnerDoc):
    id = Keyword()
    is_auto = Boolean()
    lang_code = Keyword()
    video = Nested(VideoInnerDoc)


class GeneralIndex(Document):
    # define the fields here
    start = Double()
    duration = Double()
    content = Text()
    prev_id = Keyword()
    next_id = Keyword()
    context = Text()
    caption = Nested(CaptionInnerDoc)

    class Index:
        name = "general_idx"
        # using the default settings for now.

    def save(self, **kwargs):
        # do something before save here, if you wish
        return super().save(**kwargs)


# on import, create the mappings in elasticsearch
GeneralIndex.init()
