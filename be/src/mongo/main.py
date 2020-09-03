from .settings import YoutoraMongo


class Stash:
    """
    stashes data to elasticsearch index
    """
    # Number of tracks to stash at a time
    STASH_BATCH_SIZE = 100000
    # global access point
    youtora_mongo: YoutoraMongo = None

