

# the main query to be used
from src.es.restAPIs.searchAPIs.search import SearchAPI
from src.es.restAPIs.docAPIs.single import GetAPI

import re

from src.query.create import Youtora


def search_tracks(query_text,
                  chan_lang_code: str = None,
                  caption_lang_code: str = None,
                  views_boost: int = 10,
                  like_ratio_boost: int = 5,
                  subs_boost: int = 2):
    """
    # should return a list of youtube urls,
    # each starting with the exact moment the track is uttered!
    :param caption_lang_code:
    :param chan_lang_code:
    :param query_text: the text to search for
    :param views_boost:
    :param like_ratio_boost
    :param subs_boost
    :return: a list of youtube urls
    """
    search_query = {
        "bool": {
          "must": [
            {
              "match": {
                "content": query_text
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

    response = SearchAPI.get_search(query=search_query,
                                    _from=0,
                                    _size=10,
                                    index=Youtora.YOUTORA_TRACKS_IDX_NAME)
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

        # find the prev, match, next
        prev_dict = GetAPI.get_doc(
            index=Youtora.YOUTORA_TRACKS_IDX_NAME,
            _id=re.sub(r'[0-9]+$', str(match_idx - 1), track_comp_key)
        )
        next_dict = GetAPI.get_doc(
            index=Youtora.YOUTORA_TRACKS_IDX_NAME,
            _id=re.sub(r'[0-9]+$', str(match_idx + 1), track_comp_key)
        )

        if prev_dict['found']:
            prev_start = int(prev_dict['_source']['start'])
            res['prev'] = {
                'content': prev_dict['_source']['content'],
                'context': "https://youtu.be/{}?t={}".format(vid_id, prev_start)
            }

        if next_dict['found']:
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

    # return results
