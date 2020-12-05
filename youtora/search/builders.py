# here, we employ builder pattern for constructing a srch query.
import logging
from sys import stdout
from typing import Optional, List, Callable

from nltk import ngrams

from youtora.index.docs import GeneralDoc, OpensubDoc
from youtora.search.dataclasses import SrchQuery

logging.basicConfig(stream=stdout, level=logging.INFO)


# -----  builders for a SrchQuery --- #
# the builders
# first, the interface
class SrchQueryBuilder:
    # common attribute
    MIN_SHOULD_MATCH: str = "60%"
    NUM_FRAGMENTS: int = 0
    PRE_TAG: str = "<strong>"
    POST_TAG: str = "</strong>"
    # parameters for n-gram search.
    DELIM: str = " "
    N_GRAM: int = 2
    MAX_GAPS: int = 3
    ORDERED = True

    def __init__(self, text: str, from_: int, size: int):
        # a builder maintains the final product
        self.srch_query: SrchQuery = SrchQuery()
        # must-include parameters.
        self.text: str = text  # the text to search on the index.
        self.from_: int = from_
        self.size: int = size

    # this should be the first step.
    def setup_body(self):
        self.srch_query.body = {
            "query": {
                "bool": dict()  # bool to be filled.
            },
            # for pagination, we need these two properties.
            "from": self.from_,
            "size": self.size
        }

    def build_shoulds(self):
        # as of right now, just use white space tokenization
        # Q: a more reliable way of doing this?
        # use idiom merger!
        text_tokens = self.text.strip().split(self.DELIM)
        # build ngrams
        if len(text_tokens) == 1:
            # have to do this to match the format with the output of ngrams
            text_ngrams = [(text_tokens[0],)]
        else:
            text_ngrams = ngrams(sequence=text_tokens, n=self.N_GRAM)
        # construct the should query
        shoulds = [
            {
                "intervals": {
                    "context": {
                        "match": {
                            "query": " ".join(text_ngram),
                            "max_gaps": self.MAX_GAPS,
                            "ordered": self.ORDERED
                        }  # match
                    }  # context
                }  # intervals
            }  # intervals query
            for text_ngram in text_ngrams
        ]  # should query
        # update shoulds
        self.srch_query.body['query']['bool'].update(
            {"should": shoulds}
        )

    def build_minimum_should_match(self):
        self.srch_query.body['query']['bool'].update(
            {"min_should_match": self.MIN_SHOULD_MATCH}
        )

    def build_highlight(self):
        # update highlight.
        self.srch_query.body.update(
            {
                "highlight": {
                    "context": {
                        "number_of_fragments": self.NUM_FRAGMENTS,
                        "pre_tags": [self.PRE_TAG],
                        "post_tags": [self.POST_TAG]
                    }
                }
            }
        )

    def build_steps(self) -> List[Callable]:
        raise NotImplementedError


class GeneralSrchQueryBuilder(SrchQueryBuilder):
    # keep the name of the index here.
    IDX_NAME: str = GeneralDoc.Index.name

    def __init__(self, text: str, from_: int, size: int, is_auto: bool = None,
                 capt_lang_code: str = None, chan_lang_code: str = None):
        super(GeneralSrchQueryBuilder, self).__init__(text, from_, size)
        # set the index name
        self.srch_query.idx_name = self.IDX_NAME
        # additional params for general_idx.
        self.is_auto: Optional[bool] = is_auto  # auto / manual constraint
        self.capt_lang_code: Optional[str] = capt_lang_code  # lang constraint for captions
        self.chan_lang_code: Optional[str] = chan_lang_code  # lang constraint for the channel

    def build_filters(self):
        """
        As for general search, we need builder for filters.

        :return:
        """
        filters = list()  # this may be empty.
        if isinstance(self.is_auto, bool):
            filters.append(
                {
                    'term': {
                        'caption.is_auto': self.is_auto
                    }
                }
            )
        if isinstance(self.capt_lang_code, str):
            filters.append(
                {
                    'term': {
                        'caption.lang_code': self.capt_lang_code
                    }
                }
            )
        if isinstance(self.chan_lang_code, str):
            filters.append(
                {
                    'term': {
                        'caption.video.channel.lang_code': self.chan_lang_code
                    }
                }
            )

        # build filters into body.
        self.srch_query.body['query']['bool'].update(
            {"filter": filters}
        )

    def build_steps(self) -> List[Callable]:
        """
        srch query for general_idx has its own order for building the steps.
        :return:
        """
        steps = [
            self.setup_body,  # setup_body must come first.
            self.build_shoulds,
            self.build_filters,  # as for general_idx, we include filters.
            self.build_minimum_should_match,
            self.build_highlight
        ]
        return steps


class OpensubSrchQueryBuilder(SrchQueryBuilder):
    # keep the name of the index.
    IDX_NAME: str = OpensubDoc.Index.name

    def __init__(self, text: str, from_: int, size: int):
        super().__init__(text, from_, size)
        # make sure you pass in the index name.
        self.srch_query.idx_name = self.IDX_NAME

    def build_steps(self) -> List[Callable]:
        """
        srch query  for OpenSub has its own order for building the steps.
        :return:
        """
        steps = [
            self.setup_body,  # setup_body must come first.
            self.build_shoulds,
            self.build_minimum_should_match,
            self.build_highlight
        ]
        return steps


# --- builders for a SrchResult --- #
class SrchResBuilder:

    def build_steps(self) -> List[Callable]:
        """
        to be implemented by subclasses.
        :return:
        """
        raise NotImplementedError
