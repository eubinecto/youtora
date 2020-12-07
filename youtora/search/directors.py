from youtora.search.builders import SrchQueryBuilder, Builder, SrchResBuilder, ResEntryBuilder
from youtora.search.dataclasses import SrchQuery, SrchRes, ResEntry


class Director:
    def __init__(self, builder: Builder):
        self.builder: Builder = builder

    def construct(self):
        for step in self.builder.steps:
            # execute build steps, step-by-step.
            step()


class SrchQueryDirector(Director):

    def __init__(self, builder: SrchQueryBuilder):
        super().__init__(builder)

    @property
    def srch_query(self) -> SrchQuery:
        self.builder: SrchQueryBuilder  # type cast hinting
        return self.builder.srch_query


class ResEntryDirector(Director):

    def __init__(self, builder: ResEntryBuilder):
        super().__init__(builder)

    @property
    def res_entry(self) -> ResEntry:
        self.builder: ResEntryBuilder  # type cast hinting
        return self.builder.res_entry


class SrchResDirector(Director):

    def __init__(self, builder: SrchResBuilder):
        super().__init__(builder)

    @property
    def srch_res(self) -> SrchRes:  # this is just a getter.
        self.builder: SrchResBuilder  # type cast hinting
        return self.builder.srch_res
