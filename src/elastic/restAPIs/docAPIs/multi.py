import json

from src.es.restAPIs.API import API
import requests


class BulkAPI(API):
    """
    Performs multiple indexing or delete operations in a single API call.
    This reduces overhead and can greatly increase indexing speed.
    https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html
    """
    # to be used with post request
    @classmethod
    def post_bulk(cls,
                  request_body: list,
                  refresh: str = None,
                  index=None):
        # build the query
        if index:
            query = "/_bulk"
        else:
            query = "/{index}/_bulk".format(index=index)

        params = dict()
        assert refresh in cls.REFRESH_OPS
        if refresh:
            params["refresh"] = refresh

        headers = {
            # new-line delimited json
            "Content-Type": "application/x-ndjson"
        }
        request_serialised = "\n".join([json.dumps(data) for data in request_body])
        # terminate it by a newline
        request_serialised += "\n"
        r = requests.post(url=super().ES_ENDPOINT_LOCAL + query,
                          data=request_serialised,
                          params=params,
                          headers=headers)

        # check if the request was successful
        super().Utils.log_response(r, "post_bulk")
