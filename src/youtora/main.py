import logging

from src.youtora.youtube.builders import CaptionBuilder
from src.youtora.youtube.dloaders import VideoDownloader
from src.youtora.youtube.models import Channel, Video
from src.youtora.youtube.scrapers import Scraper, ChannelScraper

from src.elastic.main import Index

from pymongo.errors import DuplicateKeyError, BulkWriteError

import numpy as np

from src.mongo.settings import YoutoraMongo


class Store:
    """
    all the main scripts for storing youtora_coll
    """
    # process batch size
    BATCH_SIZE = 10

    youtora_mongo: YoutoraMongo = None

    @classmethod
    def store_youtora_db(cls,
                         channel_url: str,
                         lang_code: str):
        """
        scrapes the desired information from the given channel url
        this is the main function to be used
        and stores it in the local mongoDB.
        :param channel_url:
        :param lang_code: the language of the channel. need this info on query time.
        """
        # check  pre-condition
        assert lang_code in CaptionBuilder.LANG_CODES_TO_COLLECT, "the lang code is invalid"
        logger = logging.getLogger("exec_idx_channel")
        # init the clients
        cls.youtora_mongo = YoutoraMongo()

        # get the driver
        driver = Scraper.get_driver(is_silent=True, is_mobile=True)
        try:
            # try scraping the channel
            # this will get the video ids of all uploaded videos
            channel = ChannelScraper.scrape_channel(channel_url, lang_code, driver=driver)
        finally:
            # always quit the driver regardless of what happens
            logger.info("closing the selenium driver")
            driver.quit()

        # split the video ids into batches
        batches = np.array_split(channel.vid_id_list, cls.BATCH_SIZE)
        for idx, batch in enumerate(batches):
            vid_gen = VideoDownloader.dl_videos_lazy(vid_id_list=batch,
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
    def _store_channel(cls,
                       channel: Channel,
                       overwrite: bool = True):
        """
        store the given channel in MongoDB.
        :param channel:
        :param overwrite:
        :return:
        """
        logger = logging.getLogger("_store_channel")
        # build the doc
        doc = {
            "_id": channel.id,
            "url": channel.url,
            "title": channel.title,
            "subs": channel.subs,
            "lang_code": channel.lang_code
        }
        # before and update
        # what was that exception?
        try:
            cls.youtora_mongo.channel_coll.insert_one(document=doc)
        except DuplicateKeyError as dke:
            if not overwrite:
                raise dke
            else:
                logger.warning(str(dke))
                # delete the channel and then reinsert
                cls.youtora_mongo.channel_coll.delete_one(filter={"_id": channel.id})
                cls.youtora_mongo.channel_coll.insert_one(document=doc)
                logger.info("channel overwritten: " + str(channel))
        else:
            logger.info("channel stored: " + str(channel))

    @classmethod
    def _store_video(cls,
                     video: Video,
                     overwrite: bool = True):
        """
        store the given video in MongoDB.
        :param video:
        :param overwrite:
        :return:
        """
        logger = logging.getLogger("_store_videos")
        # downloading the video will be initiated here
        doc = {
            # should add this field
            "_id": video.id,
            "parent_id": video.parent_id,
            "url": video.url,
            "title": video.title,
            "publish_date": video.publish_date,
            "views": video.views,
            "likes": video.likes,
            "dislikes": video.dislikes,
            "category": video.category
        }  # doc
        try:
            cls.youtora_mongo.video_coll.insert_one(document=doc)
        except DuplicateKeyError as dke:
            if not overwrite:
                raise dke
            else:
                logger.warning(str(dke))
                # delete the video and reinsert
                cls.youtora_mongo.video_coll.delete_one(filter={"_id": video.id})
                cls.youtora_mongo.video_coll.insert_one(document=doc)
                logger.info("video overwritten: " + str(video))

        else:
            logger.info("video stored: " + str(video))

    @classmethod
    def _store_captions_of(cls,
                           video: Video,
                           overwrite: bool = True):
        """
        store all tracks of the given video in MongoDB.
        :param video:
        :param overwrite:
        :return:
        """
        logger = logging.getLogger("_store_captions")
        docs = list()
        for caption in video.captions:
            doc = {
                # video is the parent of caption
                "_id": caption.id,
                "parent_id": caption.parent_id,
                "url": caption.url,
                "lang_code": caption.lang_code,
                "is_auto": caption.is_auto
            }
            docs.append(doc)
            del caption  # memory management
        # insert all captions
        try:
            cls.youtora_mongo.caption_coll.insert_many(documents=docs)
        except BulkWriteError as bwe:
            # delete all those tracks
            if not overwrite:
                raise bwe
            else:
                logger.warning(str(bwe))
                # delete and overwrite
                cls.youtora_mongo.caption_coll.delete_many(filter={"_id": {"$in": [doc["_id"] for doc in docs]}})
                cls.youtora_mongo.caption_coll.insert_many(documents=docs)
                logger.info("All captions overwritten: " + str(video))
        else:
            logger.info("All captions stored: " + str(video))

    @classmethod
    def _store_tracks_of(cls,
                         video: Video,
                         overwrite: bool = True):
        """
        store all tracks of the given video in MongoDB.
        """
        logger = logging.getLogger("_store_tracks")
        docs = list()
        for caption in video.captions:
            for track in caption.tracks:
                doc = {
                        "_id": track.id,
                        "parent_id": track.parent_id,
                        "start": track.start,
                        "duration": track.duration,
                        "content": track.content,
                }
                docs.append(doc)
                del track  # memory management
        try:
            # insert all tracks
            cls.youtora_mongo.track_coll.insert_many(documents=docs)
        except BulkWriteError as bwe:
            if not overwrite:
                raise bwe
            else:
                logger.warning(str(bwe))
                # delete and overwrite tracks
                cls.youtora_mongo.track_coll.delete_many(filter={"_id": {"$in": [doc["_id"] for doc in docs]}})
                cls.youtora_mongo.track_coll.insert_many(documents=docs)
                logger.info("all tracks overwritten: " + str(video))
        else:
            logger.info("all tracks stored: " + str(video))
