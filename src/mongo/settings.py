from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

# https://api.mongodb.com/python/current/tutorial.html
# mongodb uri
MONGO_URI = "mongodb://localhost:27017"


class YoutoraMongo:
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
        self.frame_coll: Collection = self.youtora_db['frame_coll']
