from src.es.restAPIs.API import API


class BulkAPI(API):
    """
    Performs multiple indexing or delete operations in a single API call.
    This reduces overhead and can greatly increase indexing speed.
    https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html
    """
    # to be used with post request
    BULK_REQUEST = "/_bulk"
    BULK_WITH_IDX_REQUEST = "/{index}/_bulk"

    @classmethod
    def post_bulk(cls):
        # 일단 이거는 나중에.
        pass