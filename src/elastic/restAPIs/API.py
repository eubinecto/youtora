import logging
import requests
import json

import sys
# https://stackoverflow.com/questions/20333674/pycharm-logging-output-colours/45534743
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class API:
    # currently the end point of elastic search is set to local host.
    # with the port number used by the elastic search.
    # change this to AWS endpoint after deploying the engine to AWS.
    ES_ENDPOINT_LOCAL = "http://localhost:9200"

    # the one to use for deployment
    ES_ENDPOINT_DEPLOY = "https://7cc32be9e722450490af8fb6942f5cf1.asia-northeast1.gcp.cloud.es.io:9243"

    # options to be used for validation
    REFRESH_OPS = ('true', 'false', 'wait_for')
    OP_TYPE_OPS = ('index', 'create')

    class Utils:
        """
        utilities to be used with API
        """
        @classmethod
        def log_response(cls,
                         r,
                         logger_name):
            """
            log the response.
            :param r: the response object
            :param logger_name: the name to be given to this logger
            """
            logger = logging.getLogger(name=logger_name)
            try:
                r.raise_for_status()
            except requests.exceptions.HTTPError as he:
                # check if this was an error
                if "error" in r.json():
                    # this was indeed a fatal error
                    # so raise the exception
                    logger.error(json.dumps(r.json(), indent=2))
                    raise he
            else:
                logger.info(json.dumps(r.json(), indent=2))

