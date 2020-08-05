

# the main query to be used
from src.es.restAPIs.searchAPIs.search import SearchAPI
from src.es.restAPIs.docAPIs.single import GetAPI

import re


def search_tracks(query_text):
    """
    # should return a list of youtube url's,
    # each starting with the exact moment the track is uttered!
    :param query_text: the text to search for
    :return: a list of youtube urls
    """
    search_query = {
        "bool": {
            "must": [
                {
                    "match": {
                        "text": query_text
                    }
                }
            ]  # must
        }
    }

    response = SearchAPI.get_search(query=search_query,
                                    _from=0,
                                    _size=20,
                                    index="youtora")
    # collect a timestamped url!
    results = list()
    for hit in response['hits']['hits']:
        track_comp_key = hit['_id']
        vid_id = track_comp_key.split("|")[0]
        match_idx = int(track_comp_key.split("|")[-1])
        match_start = int(hit['_source']['start'])

        res = {
            'match': {
                'text': hit['_source']['text'],
                'context': "https://youtu.be/{}?t={}".format(vid_id, match_start)
            }  # match
        }  # res

        # find the prev, match, next
        prev_dict = GetAPI.get_doc(
            index="youtora",
            _id=re.sub(r'[0-9]+$', str(match_idx - 1), track_comp_key)
        )
        next_dict = GetAPI.get_doc(
            index="youtora",
            _id=re.sub(r'[0-9]+$', str(match_idx + 1), track_comp_key)
        )

        if prev_dict['found']:
            prev_start = int(prev_dict['_source']['start'])
            res['prev'] = {
                'text': prev_dict['_source']['text'],
                'context': "https://youtu.be/{}?t={}".format(vid_id, prev_start)
            }

        if next_dict['found']:
            next_start = int(next_dict['_source']['start'])
            res['next'] = {
                'text': next_dict['_source']['text'],
                'context': "https://youtu.be/{}?t={}".format(vid_id, next_start)
            }

        # print them out
        if 'prev' in res:
            print("prev : ", end="")
            print(res['prev']['text'], "\t", res['prev']['context'])

        print("match: ", end="")
        print(res['match']['text'], "\t", res['match']['context'])

        if 'next' in res:
            print("next : ", end="")
            print(res['next']['text'], "\t", res['next']['context'])
        print("---")
        results.append(res)

    return results
