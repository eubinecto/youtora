import logging
from typing import List

from src.youtube.dload.dloaders import VideoDownloader
from src.youtube.dload.models import Video, Caption
from src.query.index import IdxSingle, IdxMulti
import pickle
import json
import subprocess
import time
from selenium import webdriver
# set the logging mode from here
# https://stackoverflow.com/questions/11548674/logging-info-doesnt-show-up-on-console-but-warn-and-error-do/11548754
from src.youtube.scrape.scrapers import ChannelScraper, Scraper

logging.basicConfig(level=logging.INFO)


class Helper:
    @classmethod
    def help_dl_vids(cls,
                     vid_id_list: List[str],
                     driver: webdriver.Chrome,
                     lang_code: str) -> List[Video]:
        # download videos
        # make this faster using multiple processes
        # total_vid_cnt = len(vid_id_list)
        # vid_done = 0
        # vid_logger = logging.getLogger("help_dl_vids")

        # do this with multiprocessing
        proc = subprocess.Popen(
            [
                "python3",
                "-m",
                "src.main.multi_proc_dl_vids",
                lang_code,
                str(10),  # num_proc
            ],
            stdout=subprocess.PIPE
        )
        # write to in
        with open("src/main/in_json.json", "w") as fh:
            fh.write(json.dumps(vid_id_list))

        # wait for this to finish.
        proc.wait()
        # read the output file
        # read byte
        with open("src/main/out.txt", 'rb') as fh:
            video_list = pickle.loads(fh.read())

        return video_list

    @classmethod
    def help_idx_vids(cls, video_list: List[Video]):
        for video in video_list:
            IdxSingle.idx_video(video)

    @classmethod
    def help_idx_captions(cls, video_list: List[Video]):
        """
        use bulk api to index captions later.
        define a generator function inside this func.
        :param video_list:
        :return:
        """
        # index all captions
        for video in video_list:
            for caption_type, caption in video.captions.items():
                caption_type: str
                caption: Caption
                IdxSingle.idx_caption(caption)

    @classmethod
    def help_idx_tracks(cls, video_list: List[Video]):
        for vid in video_list:
            for _, caption in vid.captions.items():
                caption: Caption
                IdxMulti.idx_tracks(caption.tracks,
                                    # automatically replaces the doc should it already exists
                                    op_type='index')


class Executor:
    @classmethod
    # so, we are not using idx_playlist
    def exec_idx_channel(cls,
                         channel_url: str,
                         lang_code: str):
        """
        :param channel_url: the url of the channel
        :param lang_code: the lang code to be used for downloading tracks
        :return:
        """
        # download the channel's meta data, and make it into a channel object.
        # this may change once you change the logic of dl_channel with a custom one.
        driver = Scraper.get_driver(is_silent=True,
                                    is_mobile=True)
        # scrape the channel
        channel = ChannelScraper.scrape_channel(channel_url,
                                                driver=driver)
        # dl all videos
        video_list = Helper.help_dl_vids(channel.vid_id_list,
                                         lang_code=lang_code,
                                         driver=driver)
        # close the driver after doing all that
        driver.close()
        # then start indexing
        # index the channel
        IdxSingle.idx_channel(channel)
        # index all videos
        Helper.help_idx_vids(video_list)
        # index all captions
        Helper.help_idx_captions(video_list)
        # index all tracks
        Helper.help_idx_tracks(video_list)
