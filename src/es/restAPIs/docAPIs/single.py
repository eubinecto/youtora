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
                refresh: str = None,
                op_type: str = None,
                routing: str = None):
        """
        index a document.
        :param index: (Required, string) Name of the target index.
         By default, the index is created automatically if it doesn’t exist.
        :param _id: (Optional, string) Unique identifier for the document.
        :param doc: the doc json dict.
        :param refresh: force update
        :param op_type: (Optional, enum) Set to create to only index the document
         if it does not already exist (put if absent).
        :param routing: (Optional, string) Target the specified primary shard
        """
        PUT_DOC = "/{index}/_doc/{_id}"
        query = PUT_DOC.format(index=index,
                               _id=_id)

        params = dict()

        if refresh:
            params["refresh"] = refresh
        if op_type:
            assert op_type in cls.OP_TYPE_OPS
            params["op_type"] = op_type
        if routing:
            # error check
            assert refresh in cls.REFRESH_OPS
            params["routing"] = routing

        r = requests.put(url=super().ES_ENDPOINT + query,
                         json=doc,
                         params=params)

        # check if the request was successful
        super().Utils.log_response(r, "create_doc")
