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

        # add captions
        # this doesn't require any download
        video.add_captions()

        # then return the video
        return video

    @classmethod
    def dl_videos(cls, vid_id_list: List[str]) -> List[Video]:
        """
        given a list of video ids, downloads video objects.
        :param vid_id_list:
        :return:
        """
        # download videos
        # make this faster using multiple processes
        vids = list()
        total_vid_cnt = len(vid_id_list)
        vid_done = 0
        # https://stackoverflow.com/questions/11548674/logging-info-doesnt-show-up-on-console-but-warn-and-error-do/11548754
        vid_logger = logging.getLogger("help_dl_vids")
        # 여기를 multi-processing 으로?
        # 어떻게 할 수 있는가?
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
                vids.append(video)
                vid_done += 1
                vid_logger.info("dl vid objects done: {}/{}".format(vid_done, total_vid_cnt))
        else:
            # if there are no video id's, just yield an empty list
            return vids


class TrackDownloader:
    @classmethod
    def dl_tracks(cls, vid_list: List[Video]) -> List[Track]:
        """
        this is where most of the errors occur.
        make sure to refactor this later in such a way that this is
        robust to all potential errors.
        :param vid_list:
        :return: a list of Track objects
        """
        tracks = list()
        for vid in vid_list:
            for caption in vid.captions:
                caption_comp_key = caption.caption_comp_key
                caption_url = caption.url

                logger = logging.getLogger("dl_tracks")
                # first, get the response (download)
                response = requests.get(caption_url)
                # check if the response was erroneous
                response.raise_for_status()
                # get the xml. escape the character reference entities
                tracks_xml = html.unescape(response.text)
                # deserialize the xml to dict
                tracks_dict = xmltodict.parse(tracks_xml)
                # prepare a bucket for tracks
                # get the tracks
                # error handling for the case when there is only 1 track.
                # quirk of youtube_dl
                # e.g. https://www.youtube.com/watch?v=1SMmc9gQmHQ
                if isinstance(tracks_dict['transcript']['text'], dict):
                    # just one item
                    start = float(tracks_dict['transcript']['text']["@start"])
                    try:
                        duration: float = float(tracks_dict['transcript']['text']["@dur"])
                    except KeyError as ke:
                        # duration may not exist
                        logger.warning(ke)
                        # if duration does not exist, then it is zero
                        duration = 0.0
                    try:
                        text = tracks_dict['transcript']['text']["#text"]
                    except KeyError as ke:
                        logger = logging.getLogger("@text")
                        # log the error
                        logger.warning(ke)
                        # but execution should continue
                        # empty string to state an error
                        text = ""
                    # there is only one item, so the id should end with 0.
                    track_comp_key = "|".join([caption_comp_key, '0'])
                    tracks.append(Track(track_comp_key=track_comp_key,
                                        parent_id=caption_comp_key,
                                        start=start,
                                        duration=duration,
                                        content=text))
                else:
                    for idx, trackItem in enumerate(tracks_dict['transcript']['text']):
                        start: float = float(trackItem["@start"])
                        try:
                            duration: float = float(trackItem["@dur"])
                        except KeyError as ke:
                            # duration may not exist
                            logger.warning(ke)
                            # if duration does not exist, then it is zero
                            duration = 0.0
                        try:
                            text = trackItem["#text"]
                        except KeyError as ke:
                            # log the error
                            logger.warning(ke)
                            # but execution should continue
                            # empty string to state an error
                            text = ""
                        # adding the index instead of start is crucial
                        # for quickly referencing prev & next track.
                        track_comp_key = "|".join([caption_comp_key, str(idx)])

                        # generate the track
                        tracks.append(Track(track_comp_key=track_comp_key,
                                            parent_id=caption_comp_key,
                                            start=start,
                                            duration=duration,
                                            content=text))

        else:
            # on successful completion of getting all the tracks
            # return the result
            return tracks




