# the models that I'll be using.
from typing import List, Generator

from .models import Video, Caption, Track
# how do I use type aliases?
import xmltodict

# for getting the xml caption from timed text api.
import requests

# use youtube_dl for getting the automatic captions
import youtube_dl


# to be raised when no caption was found
from .errors import CaptionNotFoundError

# for escaping character reference entities
import html

from src.youtora.youtube.scrapers import VideoScraper
import logging
import sys


# https://stackoverflow.com/questions/20333674/pycharm-logging-output-colours/45534743
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class VideoDownloader:
    # get all of the captions, whether it be manual or auto.
    VIDEO_DL_OPTS = {
        'writesubtitles': True,
        'allsubtitles': True,
        'writeautomaticsub': True,
        'writeinfojson': True,
        'quiet': True
    }  # VIDEO_DL_OPTIONS

    @classmethod
    def dl_video(cls, vid_url: str) -> Video:
        """
        given youtube video url, returns the meta data of the channel
        :param vid_url: the url of the video
        :return: a Video object
        """
        logger = logging.getLogger("dl_video")
        # get the info.
        with youtube_dl.YoutubeDL(cls.VIDEO_DL_OPTS) as ydl:
            info = ydl.extract_info(url=vid_url, download=False)

        # access the results
        vid_id = info['id']
        title = info['title']
        channel_id = info['channel_id']
        upload_date = "{year}-{month}-{day}" \
            .format(year=info['upload_date'][:4],
                    month=info['upload_date'][4:6],
                    day=info['upload_date'][6:])  # e.g. 20200610 -> 2020-06-10
        manual_sub_info = info['subtitles']
        auto_sub_info = info['automatic_captions']
        views = info['view_count']
        # the length is always greater than zero
        # use the first one as the category of this video
        category = info['categories'][0]

        # better collect these info separately
        likes, dislikes = VideoScraper.likes_dislikes(vid_url)

        # creates a video object
        video = Video(vid_id=vid_id,
                      title=title,
                      channel_id=channel_id,
                      publish_date=upload_date,
                      likes=likes,
                      dislikes=dislikes,
                      views=views,
                      category=category,
                      manual_sub_info=manual_sub_info,
                      auto_sub_info=auto_sub_info)

        # download the tracks
        done = 0
        total = len(video.captions)
        for idx, caption in enumerate(video.captions):
            caption.dl_tracks()
            done += 1
            logger.info("({}/{}), downloading tracks complete for caption:{}"
                        .format(done, total, caption))

        # then return the video
        return video

    @classmethod
    def dl_videos(cls, vid_id_list: List[str]) -> Generator[Video, None, None]:
        """
        given a list of video ids, downloads video objects.
        only yields values
        :param vid_id_list:
        :return:
        """
        total_vid_cnt = len(vid_id_list)
        vid_done = 0
        # https://stackoverflow.com/questions/11548674/logging-info-doesnt-show-up-on-console-but-warn-and-error-do/11548754
        vid_logger = logging.getLogger("help_dl_vids")
        # 여기를 multi-processing 으로?
        # 어떻게 할 수 있는가?
        if not len(vid_id_list):
            # if there are no ids, then yield None
            yield None
        else:
            for vid_id in vid_id_list:
                # make a vid_url
                vid_url = "https://www.youtube.com/watch?v={}" \
                    .format(vid_id)
                try:
                    video = VideoDownloader.dl_video(vid_url=vid_url)
                except youtube_dl.utils.DownloadError as de:
                    # if downloading the video fails, just skip this one
                    vid_logger.warning(de)
                    continue
                else:
                    # yield the video
                    yield video
                    vid_done += 1
                    vid_logger.info("dl vid objects done: {}/{}".format(vid_done, total_vid_cnt))




