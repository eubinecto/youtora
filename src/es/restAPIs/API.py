import logging
import requests
import json


class API:
    # currently the end point of elastic search is set to local host.
    # with the port number used by the elastic search.
    # change this to AWS endpoint after deploying the engine to AWS.
    ES_ENDPOINT = "http://localhost:9200"

    class Utils:
        """
        utilities to be used with API
        """
        @classmethod
        def log_response(cls,
                         r,
                         logger_name):
            """
            :param r: the response object
            :param logger_name: the name to be given to this logger
            """
            logger = logging.getLogger(name=logger_name)
            try:
                r.raise_for_status()
            except requests.exceptions.HTTPError as he:
                # log the error, just for debugging purposes
                logger.error(he)
                logger.error(json.dumps(r.json(), indent=2))
                # then raise the exception again
                raise he
            else:
                logger.info(print(json.dumps(r.json(), indent=2)))

