from typing import List

from config.settings import STR_FORMATS
from youtora.index.docs import GeneralDoc
from youtora.refine.dataclasses import Track
from youtora.search.dataclasses import SrchResult


class SrchResultsExtractor:
    VID_TIMED_URL_FORMAT = STR_FORMATS['vid_timed_url']

    @classmethod
    def parse(cls, resp_json: dict) -> List[SrchResult]:
        """
        :param resp_json: the source dictionary returned from SearchGeneralDoc.exec()
        :return:
        """
        srch_results = list()
        for hit_json in resp_json['hits']['hits']:
            # get the source
            src_json = hit_json['_source']
            # collect the tracks
            tracks = list()
            curr_track = cls._ext_track(src_json)
            tracks.append(curr_track)
            if curr_track.prev_id:
                # get the previous track
                prev_track_doc = GeneralDoc.get(id=curr_track.prev_id)
                tracks.insert(0, cls._ext_track(prev_track_doc.to_dict()))
            if curr_track.next_id:
                # get the next track
                next_track_doc = GeneralDoc.get(id=curr_track.next_id)
                tracks.append(cls._ext_track(next_track_doc.to_dict()))
            # build a search result
            srch_res = SrchResult(tracks=tracks,
                                  highlight=hit_json['highlight']['context'][0],
                                  features=src_json['caption'])
            srch_results.append(srch_res)
            del tracks
        else:
            return srch_results

    @classmethod
    def _ext_track(cls, src_json: dict) -> Track:
        # parse timed_url
        timed_url = cls.VID_TIMED_URL_FORMAT.format(
            src_json['caption']['video']['id'],
            int(src_json['start'])
        )
        # construct a track and return
        return Track(caption_id=src_json['caption']['id'],
                     start=src_json['start'],
                     duration=src_json['duration'],
                     content=src_json['content'],
                     context=src_json['context'],
                     prev_id=src_json.get('prev_id', None),
                     next_id=src_json.get('next_id', None),
                     timed_url=timed_url)
