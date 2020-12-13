import copy
from typing import Optional

from youtora.search.builders import SrchQueryBuilder, Builder, ResEntryBuilder
from youtora.search.dataclasses import SrchQuery, ResEntry


class Director:
    def __init__(self):
        self.builder: Optional[Builder] = None

    def construct(self, builder: Builder):
        self.builder = builder
        for step in self.builder.steps:
            # execute build steps, step-by-step.
            step()


class SrchQueryDirector(Director):
    """
    director to handle srch query builder
    """

    @property
    def srch_query(self) -> SrchQuery:
        self.builder: SrchQueryBuilder  # type cast hinting
        return copy.deepcopy(self.builder.srch_query)


class ResEntryDirector(Director):
    """
    director to handle res entry builder
    """

    @property
    def res_entry(self) -> ResEntry:
        self.builder: ResEntryBuilder  # type cast hinting
        return copy.deepcopy(self.builder.res_entry)
