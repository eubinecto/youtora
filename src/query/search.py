

# the main query to be used
from src.es.restAPIs.searchAPIs.search import SearchAPI


def search_tracks(query_text):
    """
    # should return a list of youtube url's,
    # each starting with the exact moment the track is uttered!
    :param query_text: the text to search for
    :return: a list of youtube urls
    """
    r_json_dict = SearchAPI.get_search(field="text",
                                       query=query_text,
                                       index="youtora")
    # collect a timestamped url!
    results = list()
    for hit in r_json_dict['hits']['hits']:
        vid_id = hit['_id'].split("|")[0]
        start_int = int(hit['_source']['start'])
        res = {
            'text': hit['_source']['text'],
            'context': "https://youtu.be/{vid_id}?t={start_int}".format(vid_id=vid_id,
                                                                        start_int=start_int)
        }
        results.append(res)

    return results
