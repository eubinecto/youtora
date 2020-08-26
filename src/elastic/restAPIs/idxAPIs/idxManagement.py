import requests
from src.elastic.restAPIs import API


class CreateIdxAPI(API):
    """
    Creates a new index.
    https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html
    """

    @classmethod
    def create_idx(cls,
                   index: str,
                   settings: dict = None,
                   alias: dict = None,
                   mappings: dict = None):
        """
        :param index: required. The name of the index to create
        :param mappings: Optional, mapping object) Mapping for fields in the index.
        :param settings: (Optional, index setting object) Configuration options for the index.
        :param alias: (Optional, alias object) Index aliases which include the index.
        """
        # build the request body
        request_body = dict()
        if settings:
            request_body["settings"] = settings
        if alias:
            request_body["alias"] = alias
        if mappings:
            request_body["mappings"] = mappings

        # send the request
        r = requests.put(url=super().ES_ENDPOINT_LOCAL + "/{index}".format(index=index),
                         json=request_body)
        # log it
        super().Utils.log_response(r, "create_idx")
        # if no exception is thrown, then return the json
        return r.json()


class DeleteIdxAPI(API):
    DEL_IDX = "/{index}"

    @classmethod
    def delete_idx(cls,
                   index: str):
        """
        deletes the index with the given name
        :param index: the name of the index to delete
        :return : the response from es
        """
        # send the request
        r = requests.delete(url=super().ES_ENDPOINT_LOCAL + "/{index}".format(index=index))
        # log it
        super().Utils.log_response(r, "delete_idx")
        # if no exception is thrown, then return the json
        return r.json()


class GetIdxAPI(API):
    """
    https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-get-index.html
    """
    GET_IDX = "/{index}"

    @classmethod
    def get_idx(cls,
                index: str):
        """
        :param index: the name of the index to get
        :return: the response from es
        """
        # send the request
        r = requests.get(url=super().ES_ENDPOINT_LOCAL + "/{index}".format(index=index))
        # log it
        super().Utils.log_response(r, "delete_idx")
        # if no exception is thrown, then return the json
        return r.json()