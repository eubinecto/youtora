import logging
from typing import List

from src.youtora.youtube.dloaders import VideoDownloader, CaptionDownloader
from src.youtora.youtube.models import Channel, Video, Caption, Track
from src.youtora.youtube.scrapers import Scraper, ChannelScraper


class Store:
    """
    all the main scripts for storing youtora_coll
    """
    @classmethod
    def store_youtora_coll(cls,
                           channel_url: str,
                           lang_code: str):
        """
        scrapes the desired information from the given channel url
        and stores it in the local mongoDB.
        :param channel_url:
        :param lang_code: the language of the channel. need this info on query time.
        """
        # pre condition
        assert lang_code in CaptionDownloader.LANG_CODES_TO_COLLECT, "the lang code is invalid"

        logger = logging.getLogger("exec_idx_channel")
        # download the channel's meta data, and make it into a channel object.
        # this may change once you change the logic of dl_channel with a custom one.
        driver = Scraper.get_driver(is_silent=True,
                                    is_mobile=True)
        # scrape the channel
        try:
            channel = ChannelScraper.scrape_channel(channel_url,
                                                    lang_code,
                                                    driver=driver)
        finally:
            # always close the driver
            # regardless of what happens
            # close the driver after doing all that
            logger.info("closing the selenium driver")
            # use quit, instead of close
            driver.quit()

        # dl all videos
        vid_list = VideoDownloader.dl_videos(vid_id_list=channel.vid_id_list)

        # dl all caption with tracks.
        caption_list = CaptionDownloader.dl_captions(vid_list)

        # stores the channel
        cls._store_channel(channel)
        # stores all videos
        cls._store_videos(vid_list)
        # store all the captions
        cls._store_captions(caption_list)
        # store all the tracks
        for caption in caption_list:
            cls._store_tracks(caption.tracks)

    @classmethod
    def _store_channel(cls, channel: Channel):
        pass

    @classmethod
    def _store_videos(cls, vid_list: List[Video]):
        # stores all the videos
        pass

    @classmethod
    def _store_captions(cls, caption_list: List[Caption]):
        # this part stores tracks as well
        # does mongoDB also support something like bulk API in elastic search?
        # first, stores the captions
        pass

    @classmethod
    def _store_tracks(cls, track_list: List[Track]):
        """
        stores all listed tracks.
        :param track_list:
        """
        pass

