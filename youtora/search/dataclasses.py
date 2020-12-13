# each dataclasses has dedicated builders in builders.py
from dataclasses import dataclass, field
from typing import Optional, List

# this is the object that we want to build
from config.settings import IndexName


@dataclass
class SrchQuery:
    body: dict = field(default_factory=dict)  # json representation of SrchQuery.
    index_name: Optional[IndexName] = None  # what index this query is for.
    # https://stackoverflow.com/q/53632152 : mutable default is not allowed for dataclasses.


@dataclass
class ResEntry:
    """
    each entry of the result.
    """
    body: dict = field(default_factory=dict)  # main data
    meta: dict = field(default_factory=dict)  # meta data

    def to_dict(self) -> dict:
        return {
            'body': self.body,
            'meta': self.meta
        }


@dataclass
class SrchRes:
    """
    search result of a index.
    """
    entries: Optional[List[ResEntry]] = None  # main srch result.
    meta: dict = field(default_factory=dict)  # meta data (e.g. total hits, etc).

    def to_dict(self) -> dict:
        return {
            'entries': [entry.to_dict() for entry in self.entries],
            'meta': self.meta
        }
