from typing import Type

from elasticsearch_dsl import Search

from config.settings import ES_CLIENT
from youtora.search.builders import SrchResBuilder, SrchQueryBuilder
from youtora.search.dataclasses import SrchQuery, SrchRes
from youtora.search.directors import SrchResDirector, SrchQueryDirector


class SrchFacade:
    """
    one facade class for searching.
    """

    def __init__(self, srch_q_builder: SrchQueryBuilder,
                 srch_r_builder_type: Type[SrchResBuilder]):
        # https://stackoverflow.com/a/59883120
        # using a type as an argument.
        self.srch_q_builder = srch_q_builder
        self.srch_r_builder_type = srch_r_builder_type

    def exec(self) -> SrchRes:
        srch_query = self.construct_srch_query()
        # first, get the resp_json.
        s = Search(using=ES_CLIENT, index=srch_query.index_name.value)
        # you can just override query with a dict representing a query
        # https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#queries
        s.query = srch_query.body
        r = s.execute()
        resp_json = r.to_dict()
        return self.construct_srch_res(resp_json)

    def construct_srch_query(self) -> SrchQuery:
        # build a search query with builders & directors
        srch_q_director = SrchQueryDirector(self.srch_q_builder)
        srch_q_director.construct()  # construct a srch query.
        return srch_q_director.srch_query

    def construct_srch_res(self, resp_json: dict) -> SrchRes:
        srch_r_builder = self.srch_r_builder_type(resp_json)
        srch_r_director = SrchResDirector(srch_r_builder)
        srch_r_director.construct()
        return srch_r_director.srch_res
