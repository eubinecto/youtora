from elasticsearch_dsl import Search

from config.settings import ES_CLIENT
from youtora.search.builders import SrchQueryBuilder, ResEntryBuilder
from youtora.search.dataclasses import SrchQuery, SrchRes
from youtora.search.directors import SrchQueryDirector
from youtora.search.factories import SrchResFactory


class SrchFacade:
    """
    one facade class for searching.
    """

    def __init__(self, srch_q_builder: SrchQueryBuilder, res_e_builder: ResEntryBuilder):
        # builders needed for srch
        self.srch_q_builder = srch_q_builder
        self.res_e_builder = res_e_builder  # to be used for srch_r_builder.
        # directors needed for srch
        self.srch_q_director = SrchQueryDirector()
        self.srch_r_factory = SrchResFactory()

    def exec(self) -> SrchRes:
        srch_query = self.construct_srch_query()
        # first, get the resp_json.
        s = Search(using=ES_CLIENT, index=srch_query.index_name.value)
        # you can just override query with a dict representing a query
        # https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#queries
        # this method is what you want.
        # create a search instance from raw dict.
        s.update_from_dict(srch_query.body)  # so, that was the problem..
        r = s.execute()
        resp_json = r.to_dict()
        return self.construct_srch_res(resp_json)

    def construct_srch_query(self) -> SrchQuery:
        # build a search query with builders & directors
        self.srch_q_director.construct(self.srch_q_builder)  # construct a srch query.
        return self.srch_q_director.srch_query

    def construct_srch_res(self, resp_json: dict) -> SrchRes:
        return self.srch_r_factory.make_srch_res(resp_json, self.res_e_builder, self.srch_q_builder.srch_field)
