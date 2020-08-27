from typing import List, Generator

from src.youtora.youtube.models import Channel, Video

from elasticsearch import Elasticsearch
from src.elastic.settings import HOSTS, YOUTORA_TRACKS_IDX_NAME

from elasticsearch.exceptions import NotFoundError

import re


class Search:

    es_client: Elasticsearch = None

    @classmethod
    def search_tracks(cls,
                      text: str,
                      chan_lang_code: str = None,
                      caption_lang_code: str = None,
                      views_boost: int = 10,
                      like_ratio_boost: int = 5,
                      subs_boost: int = 2,
                      size: int = 10):

        # init the client
        cls.es_client = Elasticsearch(HOSTS)

        # build the search query
        search_query = cls._get_search_query(text,
                                             chan_lang_code,
                                             caption_lang_code,
                                             views_boost,
                                             like_ratio_boost,
                                             subs_boost)

        response = cls.es_client.search(body=search_query,
                                        index=YOUTORA_TRACKS_IDX_NAME,
                                        from_=0,
                                        size=size)

        # collect a timestamped url!
        results = list()

        for hit in response['hits']['hits']:
            track_comp_key = hit['_id']
            vid_id = track_comp_key.split("|")[0]
            match_idx = int(track_comp_key.split("|")[-1])
            match_start = int(hit['_source']['start'])

            # this is the format of the result
            res = {
                'match': {
                    'content': hit['_source']['content'],
                    'context': "https://youtu.be/{}?t={}".format(vid_id, match_start)
                }  # match
            }  # res

            # try getting the previous track
            try:
                prev_dict = cls.es_client.get(
                    index=YOUTORA_TRACKS_IDX_NAME,
                    id=re.sub(r'[0-9]+$', str(match_idx - 1), track_comp_key)
                )
            except NotFoundError as nfe:
                pass
            else:
                prev_start = int(prev_dict['_source']['start'])
                res['prev'] = {
                    'content': prev_dict['_source']['content'],
                    'context': "https://youtu.be/{}?t={}".format(vid_id, prev_start)
                }

            # try getting the next track
            try:
                next_dict = cls.es_client.get(
                    index=YOUTORA_TRACKS_IDX_NAME,
                    id=re.sub(r'[0-9]+$', str(match_idx + 1), track_comp_key)
                )
            except NotFoundError as nfe:
                pass
            else:
                next_start = int(next_dict['_source']['start'])
                res['next'] = {
                    'content': next_dict['_source']['content'],
                    'context': "https://youtu.be/{}?t={}".format(vid_id, next_start)
                }

            # print them out
            if 'prev' in res:
                print("prev : ", end="")
                print(res['prev']['content'], "\t", res['prev']['context'])

            print("match: ", end="")
            print(res['match']['content'], "\t", res['match']['context'])

            if 'next' in res:
                print("next : ", end="")
                print(res['next']['content'], "\t", res['next']['context'])

            # print these out, just to see the metrics
            print("views:", hit['_source']['caption']['video']['views'])
            print("like ratio:", hit['_source']['caption']['video']['like_ratio'])
            print("subs:", hit['_source']['caption']['video']['channel']['subs'])
            print("---")
            results.append(res)

    @classmethod
    def _get_search_query(cls,
                          text: str,
                          chan_lang_code: str,
                          caption_lang_code: str,
                          views_boost: int,
                          like_ratio_boost: int,
                          subs_boost: int) -> dict:
        search_query = {
            "bool": {
                "must": [
                    {
                        "match": {
                            "content": text
                        }
                    }
                ],
                "should": [
                    {
                        "rank_feature": {
                            "field": "caption.video.views",
                            "boost": views_boost
                        }
                    },
                    {
                        "rank_feature": {
                            "field": "caption.video.like_ratio",
                            "boost": like_ratio_boost
                        }
                    },
                    {
                        "rank_feature": {
                            "field": "caption.video.channel.subs",
                            "boost": subs_boost
                        }
                    }
                ],
                "filter": [
                ]
            }
        }

        if caption_lang_code:
            search_query['bool']['filter'].append(
                {
                    "term": {
                        "caption.lang_code": caption_lang_code
                    }
                }
            )

        # if the channel language is given
        if chan_lang_code:
            search_query['bool']['filter'].append(
                {
                    "term": {
                        "caption.video.channel.lang_code": chan_lang_code
                    }
                }
            )
        return {
            "query": search_query
        }


class Index:
    BATCH_SIZE = 100000
    es_client: Elasticsearch = None

    @classmethod
    def index_tracks(cls,
                     channel: Channel,
                     videos: List[Video]):
        # init a client
        cls.es_client = Elasticsearch(hosts=HOSTS)

        for request_body in cls._gen_youtora_tracks(channel, videos):
            cls.es_client.bulk(body=request_body,
                               index=YOUTORA_TRACKS_IDX_NAME,
                               # immediately searchable
                               refresh='true')

    @classmethod
    def _gen_youtora_tracks(cls,
                            channel: Channel,
                            videos: List[Video]) -> Generator[list, None, None]:
        request_body = list()
        for video in videos:
            for caption in video.captions:
                for track in caption.tracks:
                    # build the query
                    query = {
                        "index": {
                            "_index": YOUTORA_TRACKS_IDX_NAME,
                            "_id": track.id,
                        }  # index
                    }  # query
                    # build the doc_body
                    doc_body = {
                        "start": track.start,
                        "duration": track.duration,
                        "content": track.content,
                        "caption": {
                            "_id": caption.id,
                            "is_auto": caption.is_auto,
                            "lang_code": caption.lang_code,
                            "video": {
                                "_id": video.id,
                                "views": video.views,
                                "publish_date_int": int("".join(video.publish_date.split("-"))),
                                "category": video.category,
                                "channel": {
                                    "_id": channel.id,
                                    "subs": channel.subs,
                                    "lang_code": channel.lang_code
                                }  # channel
                            }  # video
                        }  # caption
                    }  # doc_body
                    # add likes & dislikes only if they are greater than zero.
                    if video.likes > 0 or video.dislikes > 0:
                        if video.likes > 0:
                            # add like cnt
                            doc_body['caption']['video']['likes'] = video.likes
                            # like ratio must be greater than zero as well
                            doc_body['caption']['video']['like_ratio']: float \
                                = video.likes / (video.likes + video.dislikes)
                        # dislike cnt
                        if video.dislikes > 0:
                            # add dislike cnt
                            doc_body['caption']['video']['dislikes'] = video.dislikes
                    # build the request
                    request_body.append(query)
                    request_body.append(doc_body)

                    # if it reaches the batch size, then yield the batch
                    if (len(request_body) / 2) == cls.BATCH_SIZE:
                        yield request_body
                        request_body.clear()  # empty the bucket
        else:  # on successful iteration of all videos
            if request_body:
                # if there are still more requests left, then yield it as well
                yield request_body
