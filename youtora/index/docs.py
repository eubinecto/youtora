from elasticsearch_dsl import (
    Document,
    Object,
    InnerDoc,
    Double,
    Text,
    Keyword,
    Boolean,
    RankFeature
)  # the data types needed
from elasticsearch_dsl.connections import connections

from config.settings import ELASTICSEARCH_DSL

# create a default connection to the host

es_client = connections.create_connection(hosts=ELASTICSEARCH_DSL['default']['hosts'])


class ChannelInnerDoc(InnerDoc):
    id = Keyword(required=True)
    subs = RankFeature()  # you won't really need this.
    lang_code = Keyword()


class VideoInnerDoc(InnerDoc):
    id = Keyword(required=True)
    views = RankFeature()
    # likes = RankFeature()
    # dislikes = RankFeature()
    # like_ratio = RankFeature()
    publish_date_int = RankFeature()
    category = Keyword()  # should be a keyword
    title = Text()  # might come in handy for context2def later
    channel = Object(ChannelInnerDoc)


class CaptionInnerDoc(InnerDoc):
    id = Keyword(required=True)
    is_auto = Boolean()
    lang_code = Keyword()
    video = Object(VideoInnerDoc)


class GeneralDoc(Document):
    # define the fields here
    start = Double()
    duration = Double()
    content = Text()
    prev_id = Keyword()
    next_id = Keyword()
    context = Text()
    caption = Object(CaptionInnerDoc)

    class Index:
        name = "general_idx"
        # using the default settings for now.

    def save(self, **kwargs):
        # do something before save here, if you wish
        return super().save(**kwargs)


class OpensubDoc(Document):
    # define the fields here
    response = Text()
    # contexts. array of strings. might want to make it searchable..?
    # in elastic search, there is no dedicated "array" data type.
    # every datatype can have one or more values.
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/array.html
    contexts = Text()

    class Index:
        name = "opensub_idx"

    def save(self, **kwargs):
        # do something before saving here, if you wish.
        return super().save(**kwargs)
