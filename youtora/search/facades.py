from typing import List

from elasticsearch_dsl import Search, Q

from youtora.index.docs import es_client
from youtora.search.dataclasses import SearchQuery


class SearchGeneralDoc:
    """
    facade class that houses logic for searching general query.
    """

    @classmethod
    def exec(cls, srch_query: SearchQuery) -> dict:
        """
        :param srch_query: the search query passed from the view
        :return:
        """
        # build a search instance
        srch = Search(using=es_client)
        # pagination - https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#pagination
        srch = srch[srch_query.from_:srch_query.size]
        # add query - https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#queries
        cls._add_query(srch, srch_query)
        # add filter - https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#queries
        cls._add_filter(srch, srch_query)
        # add highlight - https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#highlighting
        cls._add_highlight(srch, srch_query)
        # to send the request to elasticsearch, call execute
        response = srch.execute()
        return response.to_dict()

    @classmethod
    def _add_query(cls, srch: Search, srch_query: SearchQuery):
        # build a boolean query
        query_q = Q('bool',
                    must=cls._build_must(srch_query),
                    should=cls._build_should(srch_query))
        srch.query = query_q

    @classmethod
    def _add_highlight(cls, srch: Search, srch_query: SearchQuery):
        if srch_query.highlight:
            srch.highlight('context', number_of_fragments=0,
                           pre_tags=["<strong>"], post_tags=["</strong>"])

    @classmethod
    def _add_filter(cls, srch: Search, srch_query: SearchQuery):
        """
        dotted fields - https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#dotted-fields
        :param srch:
        :param srch_query:
        :return:
        """
        if srch_query.is_auto is not None:
            srch.filter("term", **{'caption.is_auto': srch_query.is_auto})
        if srch_query.capt_lang_code is not None:
            srch.filter("term", **{'caption.lang_code': srch_query.capt_lang_code})
        if srch_query.chan_lang_code is not None:
            srch.filter("term", **{'caption.video.channel.lang_code': srch_query.chan_lang_code})

    @classmethod
    def _build_must(cls, srch_query: SearchQuery) -> List[Q]:
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
    def _build_should(cls, srch_query: SearchQuery) -> List[Q]:
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
