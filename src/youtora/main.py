import logging
from typing import List

from src.youtora.youtube.dloaders import VideoDownloader, TrackDownloader
from src.youtora.youtube.models import Channel, Video, Track
from src.youtora.youtube.scrapers import Scraper, ChannelScraper

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


class Store:
    """
    all the main scripts for storing youtora_coll
    """
    # process batch size
    BATCH_SIZE = 10

    # https://api.mongodb.com/python/current/tutorial.html
    MONGO_URL = "mongodb://localhost:27017"

    @classmethod
    def store_youtora_db(cls,
                         channel_url: str,
                         lang_code: str):
        """
        scrapes the desired information from the given channel url
        and stores it in the local mongoDB.
        :param channel_url:
        :param lang_code: the language of the channel. need this info on query time.
        """
        # pre condition
        assert lang_code in Video.LANG_CODES_TO_COLLECT, "the lang code is invalid"

        client = MongoClient(cls.MONGO_URL)
        youtora_db: Database = client['youtora_db']
        channel_coll: Collection = youtora_db['channel_coll']
        video_coll: Collection = youtora_db['video_coll']
        caption_coll: Collection = youtora_db['caption_coll']
        track_coll: Collection = youtora_db['track_coll']

        logger = logging.getLogger("exec_idx_channel")
        # download the channel's meta data, and make it into a channel object.
        # this may change once you change the logic of dl_channel with a custom one.
        driver = Scraper.get_driver(is_silent=True,
                                    is_mobile=True)

        # scrape the channel
        try:
            # get the channel object
            # this will get the video ids of all uploaded videos
            channel = ChannelScraper.scrape_channel(channel_url,
                                                    lang_code,
                                                    driver=driver)
        except Exception as e:
            # raise an exception on failure
            raise e
        else:
            # on successful completion, store the channel
            # stores the channel
            cls._store_channel(channel_coll=channel_coll,
                               channel=channel)
            # download & store in batches
            for idx in range(0, len(channel.vid_id_list), cls.BATCH_SIZE):
                vid_id_batch = channel.vid_id_list[idx:cls.BATCH_SIZE]
                # get the videos for this batch
                vid_list = VideoDownloader.dl_videos(vid_id_list=vid_id_batch)
                # get the tracks for this batch
                track_list = TrackDownloader.dl_tracks(vid_list=vid_list)
                # stores all videos
                cls._store_videos(video_coll=video_coll,
                                  vid_list=vid_list)
                # store all the captions
                cls._store_captions(caption_coll=caption_coll,
                                    vid_list=vid_list)
                # store all the tracks of the captions
                cls._store_tracks(track_coll=track_coll,
                                  track_list=track_list)
        finally:
            # always close the driver
            # regardless of what happens
            # close the driver after doing all that
            logger.info("closing the selenium driver")
            # use quit, instead of close
            driver.quit()

    @classmethod
    def _store_channel(cls,
                       channel_coll: Collection,
                       channel: Channel):
        # build the doc
        doc = {
            "_id": channel.channel_id,
            "url": channel.url,
            "title": channel.title,
            "subs": channel.subs,
            "lang_code": channel.lang_code
        }
        # before and update
        channel_coll.update_one(filter={"_id": channel.channel_id},
                                update={"$set": doc},
                                upsert=True)

    @classmethod
    def _store_videos(cls,
                      video_coll: Collection,
                      vid_list: List[Video]):
        # stores all the videos
        docs = [
            {
                # should add this field
                "_id": video.vid_id,
                "parent_id": video.channel_id,
                "url": video.url,
                "title": video.title,
                "publish_date": video.publish_date,
                "views": video.views,
                "likes": video.likes,
                "dislikes": video.dislikes,
            }  # doc
            for video in vid_list
        ]
        video_coll.update_many(filter=[{"_id": vid_doc["_id"]} for vid_doc in docs],
                               update={"$set": docs},
                               upsert=True)

    @classmethod
    def _store_captions(cls,
                        caption_coll: Collection,
                        vid_list: List[Video]):
        # this part stores tracks as well
        # does mongoDB also support something like bulk API in elastic search?
        # first, stores the captions
        docs = list()
        for vid in vid_list:
            for caption in vid.captions:
                doc = {
                    # video is the parent of caption
                    "_id": caption.caption_comp_key,
                    "parent_id": caption.vid_id,
                    "url": caption.url,
                    "lang_code": caption.lang_code,
                    "is_auto": caption.is_auto
                }
                docs.append(doc)
        caption_coll.update_many(filter=[{"_id": caption_doc["_id"]} for caption_doc in docs],
                                 update={"$set": docs},
                                 upsert=True)

    @classmethod
    def _store_tracks(cls,
                      track_coll: Collection,
                      track_list: List[Track]):
        """
        stores all listed tracks.
        :param track_list:
        """
        docs = [
            {
                "_id": track.track_comp_key,
                "parent_id": track.parent_id,
                "start": track.start,
                "duration": track.duration,
                "content": track.content,
            }
            for track in track_list
        ]

        # updating
        track_coll.update_many(filter=[{"_id": track_doc["_id"]} for track_doc in docs],
                               update={"$set": docs},
                               upsert=True)
