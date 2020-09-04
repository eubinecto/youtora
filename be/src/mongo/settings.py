from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

# https://api.mongodb.com/python/current/tutorial.html
# mongodb uri
# using the eubinCloud's internal IP
MONGO_URI = "mongodb://192.168.219.197:27017"


class YoutoraDB:
    """
    quick setup for accessing youtora mongo DB database.
    """
    def __init__(self):
        # set up the global access points
        client = MongoClient(MONGO_URI)
        # get the database & collections that I'll be using
        self.youtora_db: Database = client['youtora_db']
        self.channel_coll: Collection = self.youtora_db['channel_coll']
        self.video_coll: Collection = self.youtora_db['video_coll']
        self.caption_coll: Collection = self.youtora_db['caption_coll']
        self.track_coll: Collection = self.youtora_db['track_coll']
        self.chapter_coll: Collection = self.youtora_db['chapter_coll']
        # self.frame_coll: Collection = self.youtora_db['frame_coll']


class CorporaDB:
    """
    quick setup for accessing corpora data set.
    """
    def __init__(self):
        # set up the global access points
        client = MongoClient(MONGO_URI)
        # get the database & collections that I'll be using
        self.corpora_db: Database = client['corpora_db']
        self.ml_gloss_raw_coll: Collection = self.corpora_db['ml_gloss_raw_coll']
        self.ml_gloss_coll: Collection = self.corpora_db['ml_gloss_coll']
