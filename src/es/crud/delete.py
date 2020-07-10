

from src.es.constants import *

import requests
import json

from src.es.utils import log_response


def delete_index(index_name):
    """
    e.g.
    DELETE /twitter
    :param index_name: the name of the index to delete.
    """
    # a simple delete request
    r = requests.delete(url=ES_END_POINT + "/{}".format(index_name))

    # log it
    log_response(r, "delete_index")

    # just return it
    return r.json()
