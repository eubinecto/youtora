# and the director. director is given a
from typing import Optional

from youtora.search.builders import SrchQueryBuilder, SrchResBuilder
from youtora.search.dataclasses import SrchQuery


class SrchQueryDirector:
    def __init__(self):
        # a director maintains a builder
        self.srch_query_builder: Optional[SrchQueryBuilder] = None

    def construct_srch_query(self, srch_query_builder: SrchQueryBuilder):
        """
        given a builder, constructs a srch query.
        :param srch_query_builder:
        :return:
        """
        # set the builder
        self.srch_query_builder = srch_query_builder
        # step-by-step construction.
        for step in self.srch_query_builder.build_steps():
            step()  # step is a callable.

    # alias to the srch_query.
    @property
    def srch_query(self) -> SrchQuery:
        return self.srch_query_builder.srch_query


class SrchResDirector:
    def __init__(self):
        self.srch_res_builder: Optional[SrchResDirector] = None

    def construct_srch_res(self, srch_res_builder: SrchResBuilder):
        self.srch_res_builder = srch_res_builder
        for step in self.srch_res_builder.build_steps():
            step()
