from typing import List

from elasticsearch_dsl import Search, Q
from nltk.util import ngrams

from youtora.index.docs import es_client
from youtora.search.dataclasses import SrchQuery, SrchResult
from youtora.search.extractors import SrchResultsExtractor


class SrchGeneralDoc:
    """
    facade class that houses logic for searching general query.
    """
    # parameters for search.
    MIN_SHOULD_MATCH = "60%"
    N_GRAM = 2
    MAX_GAPS = 3
    DELIM = " "
    ORDERED = True

    @classmethod
    def exec(cls, srch_query: SrchQuery) -> List[SrchResult]:
        """
        :param srch_query: the search query passed from the view
        :return:
        """
        resp_json = cls.build_and_exec(srch_query)
        # parse the response json to get a list of search results
        srch_results = SrchResultsExtractor.parse(resp_json)
        return srch_results

    @classmethod
    def build_and_exec(cls, srch_query: SrchQuery) -> dict:
        # build a search instance
        srch = Search(using=es_client)
        # pagination - https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#pagination
        srch = srch[srch_query.from_:srch_query.size]
        # add query - https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#queries
        srch = cls._add_query(srch, srch_query)
        # add highlight - https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#highlighting
        srch = cls._add_highlight(srch)
        # to send the request to elasticsearch, call execute
        resp_json = srch.execute()
        return resp_json.to_dict()

    @classmethod
    def _add_query(cls, srch: Search, srch_query: SrchQuery) -> Search:
        # add must, should, filter and return the search object
        q = Q(
            {
                'bool': {
                    'should': cls._build_should(srch_query),
                    'filter': cls._build_filter(srch_query),
                    'minimum_should_match': cls.MIN_SHOULD_MATCH
                }
            }
        )
        # attach a query to
        return srch.query(q)

    @classmethod
    def _add_highlight(cls, srch: Search) -> Search:
        return srch.highlight('context', number_of_fragments=0,
                              pre_tags=["<strong>"], post_tags=["</strong>"])

    @classmethod
    def _build_filter(cls, srch_query: SrchQuery) -> List[dict]:
        filters = list()
        if isinstance(srch_query.is_auto, bool):
            q = {
                'term': {
                    'caption.is_auto': srch_query.is_auto
                }
            }
            filters.append(q)
        if isinstance(srch_query.capt_lang_code, str):
            q = {
                'term': {
                    'caption.lang_code': srch_query.capt_lang_code
                }
            }
            filters.append(q)
        if isinstance(srch_query.chan_lang_code, str):
            q = {
                'term': {
                    'caption.video.channel.lang_code': srch_query.chan_lang_code
                }
            }
            filters.append(q)
        return filters

    @classmethod
    def _build_should(cls, srch_query: SrchQuery) -> List[dict]:
        """
        should boost views & subs (and later, publish_date_int)
        :param srch_query:
        :return:
        """
        # as of right now, just use white space tokenization
        text_tokens = srch_query.text.strip().split(cls.DELIM)
        # build ngrams
        if len(text_tokens) == 1:
            # have to do this to match the format with the output of ngrams
            text_ngrams = [(text_tokens[0],)]
        else:
            text_ngrams = ngrams(sequence=text_tokens, n=cls.N_GRAM)
        # construct the should query
        should = [
            {
                "intervals": {
                    "context": {
                        "match": {
                            "query": " ".join(text_ngram),
                            "max_gaps": cls.MAX_GAPS,
                            "ordered": cls.ORDERED
                        }  # match
                    }  # context
                }  # intervals
            }  # intervals query
            for text_ngram in text_ngrams
        ]  # should query
        # return the list of queries
        return should
