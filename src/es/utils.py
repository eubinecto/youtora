
import logging
import requests
import json


def log_response(r, logger_name):
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
