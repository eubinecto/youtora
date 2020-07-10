import logging

import requests
import json
from src.es.constants import *
from src.es.utils import log_response


def get_index(index_name):
    """
    e.g.
    GET /twitter
    :param index_name: the name of the index to delete.
    """
    # a simple delete request
    r = requests.get(url=ES_END_POINT + "/{}".format(index_name))

    # log it
    log_response(r, "get_index")
    return r.json()


class Search:
    """
    class to hard-code the frequently used queries
    and parsing patterns.

    """
    pass

