from typing import Optional, List

from youtora.search.builders import ResEntryBuilder
from youtora.search.dataclasses import ResEntry, SrchRes
from youtora.search.directors import ResEntryDirector


class SrchResFactory:

    def __init__(self):
        self.res_e_director = ResEntryDirector()
        # to be filled
        self.res_e_builder: Optional[ResEntryBuilder] = None
        self.resp_json: Optional[dict] = None
        self.srch_field: Optional[str] = None

    def make_srch_res(self, resp_json: dict,
                      res_e_builder: ResEntryBuilder,
                      srch_field: str) -> SrchRes:
        self.resp_json = resp_json
        self.res_e_builder = res_e_builder
        self.srch_field = srch_field
        entries = self.make_entries()
        meta = self.make_meta()
        return SrchRes(entries, meta)

    def make_entries(self) -> List[ResEntry]:
        # to be filled.
        entries: List[ResEntry] = list()
        # initialise builders and directors to use.
        for hit_json in self.resp_json['hits']['hits']:
            # make sure to give it the name for srch_field.
            self.res_e_builder.prep(hit_json, self.srch_field)
            # use the director for building General Srch Entries.
            self.res_e_director.construct(self.res_e_builder)
            res_entry = self.res_e_director.res_entry
            entries.append(res_entry)
        else:
            return entries

    @staticmethod
    def make_meta() -> dict:
        """
        :return:
        """
        # if you need any metadata to be included
        # do it here.
        meta = dict()
        return meta
