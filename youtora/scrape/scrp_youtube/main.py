import logging
from logging import Logger
from typing import List

from pymongo.collection import Collection

from .builders import CaptionBuilder
from .scrapers import VideoScraper, ChannelScraper
from .dataclasses import Channel, Video
from youtora.index.idx_general.index import GeneralIndex

# for splitting the videos into batches.
import numpy as np


import sys

# global logger setting
# https://stackoverflow.com/questions/20333674/pycharm-logging-output-colours/45534743
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# this scraper stores data directly to elasticsearch idx.


class Store:
    """
    all the main scripts for storing youtora_coll
    """
    # process batch size
    BATCH_SIZE = 10

    @classmethod
    def store_youtora_db(cls,
                         channel_url: str,
                         lang_code: str,
                         os: str = 'mac'):
        """
        scrapes the desired information from the given channel url
        this is the main function to be used
        and stores it in the local mongoDB.
        :param os:
        :param channel_url:
        :param lang_code: the language of the channel. need this info on query time.
        """
        # check  pre-condition
        assert lang_code in CaptionBuilder.LANG_CODES_TO_COLLECT, "the lang code is invalid"
        logger = logging.getLogger("store_youtora_db")
        # init the clients
        cls.youtora_db = YoutoraDB()

        # this will get the video ids of all uploaded videos
        channel = ChannelHTMLParser.parse(channel_url, lang_code, os)

        # split the video ids into batches
        batches = np.array_split(channel.vid_id_list, cls.BATCH_SIZE)
        for idx, batch in enumerate(batches):
            vid_gen = VideoScraper.scrape(vid_id_list=batch,
                                          batch_info="current={}/total={}"
                                          .format(idx + 1, len(batches)))
            for video in vid_gen:   # dl and iterate over each video in this batch
                if not video.captions:
                    logger.info("SKIP: skipping storing the video because it has no captions at all")
                    continue
                # store video, captions, and tracks
                cls._store_video(video)
                cls._store_captions_of(video)
                cls._store_tracks_of(video)
                # on storing everything, store the indices as well
                # this should be done on mongo db side, but as of right now, do it this way
                Index.index_tracks(channel=channel, videos=[video])
        else:
            # on storing all batches, store the channel. channel is stored at the end.
            cls._store_channel(channel=channel)

    @classmethod
    def _store_channel(cls, channel: Channel):
        """
        store the given channel in MongoDB.
        :param channel:
        """
        logger = logging.getLogger("_store_channel")
        # store the channel
        cls._store_one(coll=cls.youtora_db.channel_coll,
                       doc=channel.to_json(),
                       rep_id=channel.id,
                       logger=logger)

    @classmethod
    def _store_video(cls, video: Video):
        """
        store the given video in MongoDB.
        :param video:
        """
        logger = logging.getLogger("_store_videos")
        # store the video
        cls._store_one(coll=cls.youtora_db.video_coll,
                       doc=video.to_json(),
                       rep_id=video.id,
                       logger=logger)

    @classmethod
    def _store_captions_of(cls, video: Video):
        """
        store all tracks of the given video in MongoDB.
        :param video:
        """
        logger = logging.getLogger("_store_captions_of")
        docs = [caption.to_json() for caption in video.captions]
        # store all captions
        cls._store_many(coll=cls.youtora_db.caption_coll,
                        docs=docs,
                        rep_id=video.id,
                        logger=logger)

    @classmethod
    def _store_tracks_of(cls, video: Video):
        """
        store all tracks of the given video in MongoDB.
        """
        logger = logging.getLogger("_store_tracks_of")
        docs = [
            track.to_json()
            for caption in video.captions
            for track in caption.tracks
        ]  # "flattening" the list with nested list comprehension
        # store all tracks
        cls._store_many(coll=cls.youtora_db.track_coll,
                        docs=docs,
                        rep_id=video.id,
                        logger=logger)

    @classmethod
    def _store_one(cls,
                   coll: Collection,
                   doc: dict,
                   rep_id: str,
                   logger: Logger):
        if doc:
            try:
                coll.insert_one(document=doc)
            except DuplicateKeyError:
                # logger.warning(str(dke))
                # delete the channel and then reinsert
                coll.delete_one(filter={"_id": doc["_id"]})
                coll.insert_one(document=doc)
                logger.warning("overwritten: " + rep_id)
            else:
                logger.info("stored: " + rep_id)
        else:
            logger.warning("SKIP: the document is empty")

    @classmethod
    def _store_many(cls,
                    coll: Collection,
                    docs: List[dict],
                    rep_id: str,
                    logger: Logger):
        if docs:
            try:
                # insert all tracks
                coll.insert_many(documents=docs)
            except BulkWriteError:
                # logger.warning(str(bwe))
                # delete and overwrite tracks
                coll.delete_many(filter={"_id": {"$in": [doc["_id"] for doc in docs]}})
                coll.insert_many(documents=docs)
                logger.warning("all overwritten for: " + rep_id)
            else:
                logger.info("all stored for: " + rep_id)
        else:
            logger.warning("SKIP: the documents list is empty")
