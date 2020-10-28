from typing import List

from elasticsearch_dsl import Search, Q

from youtora.index.docs import es_client
from youtora.search.dataclasses import SrchQuery


class SearchGeneralDoc:
    """
    facade class that houses logic for searching general query.
    """

    @classmethod
    def exec(cls, srch_query: SrchQuery) -> dict:
        """
        :param srch_query: the search query passed from the view
        :return:
        """
        # build a search instance
        srch = Search(using=es_client)
        # pagination - https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#pagination
        srch = srch[srch_query.from_:srch_query.size]
        # add query - https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#queries
        srch = cls._add_query(srch, srch_query)
        # add highlight - https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#highlighting
        srch = cls._add_highlight(srch)
        # to send the request to elasticsearch, call execute
        response = srch.execute()
        return response.to_dict()

    @classmethod
    def _add_query(cls, srch: Search, srch_query: SrchQuery) -> Search:
        # add must, should, filter and return the search object
        return srch.query('bool',
                          must=cls._build_must(srch_query),
                          filter=cls._build_filter(srch_query))

    @classmethod
    def _add_highlight(cls, srch: Search) -> Search:
        return srch.highlight('context', number_of_fragments=0,
                              pre_tags=["<strong>"], post_tags=["</strong>"])

    @classmethod
    def _build_filter(cls, srch_query: SrchQuery) -> List[Q]:
        filters = list()
        if isinstance(srch_query.is_auto, bool):
            filters.append(Q("term", **{'caption.is_auto': srch_query.is_auto}))
        if isinstance(srch_query.capt_lang_code, str):
            filters.append(Q("term", **{'caption.lang_code': srch_query.capt_lang_code}))
        if isinstance(srch_query.chan_lang_code, str):
            filters.append(Q("term", **{'caption.video.channel.lang_code': srch_query.chan_lang_code}))
        return filters

    @classmethod
    def _build_must(cls, srch_query: SrchQuery) -> List[Q]:
        """
        must match content and context
        :param srch_query:
        :return:
        """
        must = list()
        must.append(Q('match', content=srch_query.text))
        must.append(Q('match', context=srch_query.text))
        return must

    @classmethod
    def _build_should(cls, srch_query: SrchQuery) -> List[Q]:
        """
        should boost views & subs (and later, publish_date_int)
        :param srch_query:
        :return:
        """
        should = list()
        should.append(Q('rank_feature', field="caption.video.views",
                        boost=srch_query.views_boost))
        should.append(Q('rank_feature', field='caption.video.channel.subs',
                        boost=srch_query.subs_boost))
        return should
