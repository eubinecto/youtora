# here, we employ builder pattern for constructing a srch query.
import logging
import re
from abc import ABC
from sys import stdout
from typing import Optional, List, Callable

from nltk import ngrams
from termcolor import colored

from config.settings import STR_FORMATS, IndexName  # global variables to use.
from youtora.index.docs import GeneralDoc  # for getting prev & next track.
from youtora.search.dataclasses import SrchQuery, ResEntry

logging.basicConfig(stream=stdout, level=logging.INFO)

# global constants
PRE_TAG = "<strong>"
POST_TAG = "</strong>"
BOLD_RE = re.compile(r'{}([\S ]+?){}'.format(PRE_TAG, POST_TAG))


class Builder:

    @property
    def steps(self) -> List[Callable]:
        raise NotImplementedError


# -----  builders for a SrchQuery --- #
# the builders
# first, the interface
class SrchQueryBuilder(Builder, ABC):
    # common attribute
    MIN_SHOULD_MATCH: str = "60%"
    NUM_FRAGMENTS: int = 2
    # parameters for n-gram search.
    DELIM: str = " "
    N_GRAM: int = 2
    MAX_GAPS: int = 3
    ORDERED = True

    def __init__(self):
        # a builder maintains the final product
        self.srch_query: SrchQuery = SrchQuery()
        # must-include parameters.
        self.text: Optional[str] = None
        self.from_: Optional[int] = None
        self.size: Optional[int] = None
        self.srch_field: Optional[str] = None

    def prep(self, text: str, from_: int, size: int):
        self.text: str = text  # the text to search on the index.
        self.from_: int = from_
        self.size: int = size

    # this should be the first step.
    def setup_body(self):
        self.srch_query.body.update(
            {
                "query": dict(),
                # for pagination, we need these two properties.
                "from": self.from_,
                "size": self.size
            }
        )  # update body.

    def build_bool(self):
        self.srch_query.body['query'].update(
            {
                "bool": dict()
            }
        )

    def build_match(self):
        self.srch_query.body['query'].update(
            {
                "match": {
                    self.srch_field: self.text
                }
            }
        )

    def build_shoulds(self):
        # as of right now, just use white space tokenization
        # TODO: a more reliable way of doing this? -> possible: use IdiomNLP.
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
                    self.srch_field: {
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
            {
                "should": shoulds
            }
        )

    def build_minimum_should_match(self):
        self.srch_query.body['query']['bool'].update(
            {
                "min_should_match": self.MIN_SHOULD_MATCH
            }
        )

    def build_highlight(self):
        global PRE_TAG, POST_TAG
        # update highlight.
        self.srch_query.body.update(
            {
                "highlight": {
                    "pre_tags": [PRE_TAG],
                    "post_tags": [POST_TAG],
                    "fields": {
                        self.srch_field: {
                            "number_of_fragments": self.NUM_FRAGMENTS,
                        }
                    }
                }
            }
        )


class GeneralSrchQueryBuilder(SrchQueryBuilder):

    def __init__(self):
        super(GeneralSrchQueryBuilder, self).__init__()
        # set the index name
        self.srch_query.index_name = IndexName.GENERAL
        self.srch_field = "context"
        # additional params for general_idx.
        self.is_auto: Optional[bool] = None  # auto / manual constraint
        self.capt_lang_code: Optional[str] = None  # lang constraint for captions
        self.chan_lang_code: Optional[str] = None  # lang constraint for the channel

    def prep(self, text: str, from_: int, size: int, is_auto: bool = None,
             capt_lang_code: str = None, chan_lang_code: str = None):
        super().prep(text, from_, size)
        self.is_auto = is_auto
        self.capt_lang_code = capt_lang_code
        self.chan_lang_code = chan_lang_code

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
            {
                "filter": filters
            }
        )

    @property
    def steps(self) -> List[Callable]:
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

    def __init__(self):
        super(OpensubSrchQueryBuilder, self).__init__()
        # make sure you pass in the index name.
        self.srch_query.index_name = IndexName.OPENSUB
        self.srch_field = "response"

    @property
    def steps(self) -> List[Callable]:
        """
        srch query  for OpenSub has its own order for building the steps.
        :return:
        """
        steps = [
            self.setup_body,  # setup_body must come first.
            self.build_bool,
            self.build_shoulds,
            self.build_highlight
        ]
        return steps


# --- builders for a SrchResult --- #
# do we.. really need builders here?
# wouldn't factory be better? because.. it has..
class ResEntryBuilder(Builder, ABC):

    def __init__(self):
        """
        """
        self.res_entry: ResEntry = ResEntry()
        self.hit_json: Optional[dict] = None
        self.src_json: Optional[dict] = None
        self.srch_field: Optional[str] = None

    def prep(self, hit_json: dict, srch_field: str):
        """
        :param hit_json: e.g. resp_json['hits'][['hits'][0]
        :param srch_field
        :return:
        """
        self.hit_json = hit_json
        self.src_json = hit_json['_source']
        self.srch_field = srch_field

    def build_highlight(self):
        global BOLD_RE
        # get the highlights from resp_json, and build it into body
        highlight: Optional[dict] = self.hit_json.get('highlight', None)
        if highlight:
            highlight_text = highlight[self.srch_field][0]
            hls = BOLD_RE.findall(string=highlight_text)
            for hl in hls:  # highlight the strong-tagged parts
                highlight_text = BOLD_RE.sub(repl=colored(hl, 'blue'),
                                             string=highlight_text,
                                             # sub only the first one
                                             count=1)
        else:
            highlight_text = None

        self.res_entry.body.update(
            {
                "highlight": {
                    "raw": highlight,
                    "text": highlight_text
                }
            }
        )


class GeneralResEntryBuilder(ResEntryBuilder):
    VID_TIMED_URL_FORMAT = STR_FORMATS['vid_timed_url']

    @classmethod
    def update_timed_url(cls, track_src_json: dict):
        # TODO why don't we just.. use http://... for the ids?
        # include timed_url in general_idx! (or mongodb)
        timed_url = cls.VID_TIMED_URL_FORMAT.format(
            track_src_json['caption']['video']['id'],
            int(track_src_json['start'])  # truncate the float
        )
        # update
        track_src_json.update(
            {
                'timed_url': timed_url
            }
        )

    def build_tracks(self):
        # get the tracks from src_json, and build tracks.
        self.update_timed_url(self.src_json)
        prev_id: str = self.src_json.get('prev_id', None)
        next_id: str = self.src_json.get('next_id', None)
        tracks: List[dict] = [self.src_json]
        if prev_id:
            prev_track_src_json = GeneralDoc.get(id=prev_id).to_dict()
            self.update_timed_url(prev_track_src_json)
            tracks.insert(0, prev_track_src_json)  # the first one is the prev track
        if next_id:
            next_track_src_json = GeneralDoc.get(id=next_id).to_dict()
            self.update_timed_url(next_track_src_json)
            tracks.append(next_track_src_json)  # the last one is the next track

        # update the body with tracks!
        self.res_entry.body.update(
            {
                "tracks": tracks
            }
        )

    def build_meta(self):
        # get the features from src_json, and build tracks
        # e.g. caption: ..., video: ..., channel: ...
        features: dict = self.src_json['caption']
        self.res_entry.meta.update(**features)

    @property
    def steps(self) -> List[Callable]:
        return [
            self.build_highlight,  # build highlight first.
            self.build_tracks,
            self.build_meta
        ]


class OpensubResEntryBuilder(ResEntryBuilder):

    def build_response(self):
        response: str = self.src_json['response']
        self.res_entry.body.update(
            {
                "response": response
            }
        )

    def build_contexts(self):
        contexts: List[str] = self.src_json['response']
        self.res_entry.body.update(
            {
                "contexts": contexts
            }
        )

    @property
    def steps(self) -> List[Callable]:
        return [
            self.build_highlight,  # build highlight first.
            self.build_response,
            self.build_contexts
        ]
