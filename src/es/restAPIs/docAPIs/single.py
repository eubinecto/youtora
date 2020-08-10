from src.es.restAPIs.API import API
import requests


class IdxAPI(API):
    """
    Adds a JSON document to the specified index and makes it searchable.
    If the document already exists, updates the document and increments its version.
    https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html
    """
    PUT_DOC = "/{index}/_doc/{_id}"

    @classmethod
    def put_doc(cls,
                index: str,
                _id: str,
                doc: dict,
                refresh: str = None,
                op_type: str = None,
                routing: str = None):
        """
        index a document.
        :param index: (Required, string) Name of the target index.
         By default, the index is created automatically if it doesn’t exist.
        :param _id: (Optional, string) Unique identifier for the document.
        :param doc: the doc json dict.
        :param refresh: make the fields immediately searchable.
        :param op_type: (Optional, enum) Set to create to only index the document
         if it does not already exist (put if absent).
        :param routing: (Optional, string) Target the specified primary shard
        """
        # simple assertions
        assert refresh in cls.REFRESH_OPS

        query = cls.PUT_DOC.format(index=index, _id=_id)

        params = dict()

        if refresh:
            # make it
            params["refresh"] = refresh
        if op_type:
            assert op_type in cls.OP_TYPE_OPS
            params["op_type"] = op_type
        if routing:
            # error check
            assert refresh in cls.REFRESH_OPS
            params["routing"] = routing

        r = requests.put(url=super().ES_ENDPOINT_LOCAL + query,
                         json=doc,
                         params=params)

        r.raise_for_status()

        # check if the request was successful
        super().Utils.log_response(r, "create_doc")


class GetAPI(API):
    """
    Retrieves the specified JSON document from an index.
    https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-get.html
    """
    GET_DOC = "/{index}/_doc/{_id}"

    @classmethod
    def get_doc(cls, index: str, _id: str) -> dict:
        query = cls.GET_DOC.format(index=index, _id=_id)

        r = requests.get(url=super().ES_ENDPOINT_LOCAL + query)

        # check if the request was successful
        super().Utils.log_response(r, "get_doc")

        # if that was successful, return the json
        return r.json()


class UpdateAPI(API):
    """
    Updates a document using the specified script.
    maybe try doing this with all the videos?
    https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update.html
    """
    pass
