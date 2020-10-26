from typing import List

from youtora.search.dataclasses import SearchResult


class SearchResultExtractor:

    @classmethod
    def parse(cls, resp_dict: dict) -> List[SearchResult]:
        pass
