from src.es.restAPIs.API import API
import requests


class IdxAPI(API):
    """
    Adds a JSON document to the specified index and makes it searchable.
    If the document already exists, updates the document and increments its version.
    https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html
    """
    @classmethod
    def put_doc(cls,
                index: str,
                _id: str,
                doc: dict,
                refresh: bool,
                routing: str = None):
        """
        index a document.
        :param index: (Required, string) Name of the target index.
         By default, the index is created automatically if it doesn’t exist.
        :param _id: (Optional, string) Unique identifier for the document.
        :param doc: the doc json dict.
        :param refresh: force update
        :param routing: the parent id to rout to on using relations
        """
        PUT_DOC = "/{index}/_doc/{_id}"
        query = PUT_DOC.format(index=index,
                               _id=_id)

        # need to specify the content type in the headers,
        # or else you'll get an error like this:
        # "Content-Type header [application/x-www-form-urlencoded] is not supported",
        headers = {
            "content-type": "application/json"
        }
        params = dict()
        if refresh:
            params["refresh"] = ""
        if routing:
            params["routing"] = routing

        r = requests.put(url=super().ES_ENDPOINT + query,
                         json=doc,
                         params=params,
                         headers=headers)

        # check if the request was successful
        super().Utils.log_response(r, "create_doc")
