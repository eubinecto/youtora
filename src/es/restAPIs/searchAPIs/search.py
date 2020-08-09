import requests

from src.es.restAPIs.API import API


class SearchAPI(API):
    """
    https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-body.html
    """
    @classmethod
    def get_search(cls,
                   query: dict,
                   index: str = None,
                   _from: int = 0,
                   _size: int = 100,):

        # build the request to add on
        request = "/{index}/_search".format(index=index)

        # build the request body
        request_body = {
            "from": _from,
            "size": _size,
            "query": query
        }  # request body
        # send the request
        r = requests.get(url=cls.ES_ENDPOINT_LOCAL + request,
                         json=request_body)

        # log the response
        # log it
        #super().Utils.log_response(r, "get_search")

        # if no exception is thrown, then return the json
        # this will be the search result
        return r.json()
