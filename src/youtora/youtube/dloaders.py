# the models that I'll be using.
from typing import List

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
        manual_sub_info = info['manual_sub_info']
        auto_sub_info = info['automatic_captions']
        views = info['view_count']
        # the length is always greater than zero
        # use the first one as the category of this video
        category = info['categories'][0]

        # better collect these info separately
        likes, dislikes = VideoScraper.likes_dislikes(vid_url)

        # returns a video object with the properties above
        return Video(vid_id=vid_id,
                     title=title,
                     channel_id=channel_id,
                     publish_date=upload_date,
                     likes=likes,
                     dislikes=dislikes,
                     views=views,
                     category=category,
                     manual_sub_info=manual_sub_info,
                     auto_sub_info=auto_sub_info)

    @classmethod
    def dl_videos(cls, vid_id_list: List[str]) -> List[Video]:
        """
        given a list of video ids, downloads video objects.
        :param vid_id_list:
        :return:
        """
        # download videos
        # make this faster using multiple processes
        video_list: List[Video] = list()
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
                video_list.append(video)
                vid_done += 1
                vid_logger.info("dl vid objects done: {}/{}".format(vid_done, total_vid_cnt))

        return video_list


class CaptionDownloader:
    # the caption types defined
    CAPTION_TYPES = ("manual", "auto")

    # the caption format I'll be using
    CAPTION_FORMAT = 'srv1'

    # list of caption formats
    # used by youtube_dl
    FORMAT_IDX = {
        'srv1': 0,
        'srv2': 1,
        'srv3': 2,
        'ttml': 3,
        'vtt': 4
    }

    # korean, japanese, english, british english, french
    # we are only downloading captions of these languages .
    LANG_CODES_TO_COLLECT = {'ko', 'ja', 'en', 'en-GB', 'fr'}

    @classmethod
    def dl_caption(cls,
                   video: Video,
                   caption_type: str,
                   lang_code: str):
        """
        extract the caption from the video object
        need to handle the case where the lang code does not exist.
        I think you might need to download the list of lang codes.
        :param video:
        :param caption_type: manual = manually written, auto = ASR. the default is auto.
        :param lang_code: the language code should be given
        :return: a caption object
        """
        # information I'll need
        vid_id = video.vid_id
        manual_sub_info = video.manual_sub_info
        auto_sub_info = video.auto_sub_info

        # input check - must be either  "manual" or "auto"
        if caption_type not in cls.CAPTION_TYPES:
            raise ValueError(caption_type)

        # set the desired caption format in the CaptionScraper class.
        format_idx = cls.FORMAT_IDX[cls.CAPTION_FORMAT]

        # this is initially None
        caption_url = None

        # switch statement
        if caption_type == "manual":
            if lang_code in manual_sub_info:  # manual exists
                caption_url = manual_sub_info[lang_code][format_idx]['url']
        elif caption_type == "auto":  # auto exists
            if lang_code in auto_sub_info:
                caption_url = auto_sub_info[lang_code][format_idx]['url']

        # Note: a None is a singleton object.
        # there can only be 1 None.
        # So whatever variable that is assigned to None keyword
        # refers to the same memory location. ("NULL" in C)
        # so it makes sense to use is operator rather than equality operator.
        if not caption_url:
            raise CaptionNotFoundError("NOT FOUND: {},{}"
                                       .format(caption_type, lang_code))

        # this will be the id of each caption
        caption_comp_key = "|".join([vid_id, caption_type, lang_code])

        # this part is where it will take time
        # get the tracks with the given caption url
        tracks = cls._dl_tracks(caption_comp_key=caption_comp_key,
                                caption_url=caption_url)

        # return the caption object with tracks
        return Caption(caption_comp_key=caption_comp_key,
                       vid_id=vid_id,
                       url=caption_url,
                       tracks=tracks)

    @classmethod
    def dl_captions(cls, vid_list: List[Video]) -> List[Caption]:
        """
        given a list of videos, downloads all captions for each video.
        :param vid_list:
        :return:
        """
        logger = logging.getLogger("dl_captions")

        # captions now should be a list of captions
        captions = list()

        # loop through all of the videos.
        for video in vid_list:
            for lang_code in cls.LANG_CODES_TO_COLLECT:
                try:
                    # manual
                    # first get all available manual captions.
                    caption_type = "manual"
                    manual_caption = CaptionDownloader.dl_caption(video=video,
                                                                  caption_type=caption_type,
                                                                  lang_code=lang_code)
                except CaptionNotFoundError as ce:
                    logger.info(str(ce))
                    # try getting an automatic one
                    try:
                        caption_type = "auto"
                        auto_caption = CaptionDownloader.dl_caption(video=video,
                                                                    caption_type=caption_type,
                                                                    lang_code=lang_code)
                    except CaptionNotFoundError as ce:
                        # automatic one was not found either
                        logger.info(str(ce))
                    else:
                        # collect the automatic caption
                        captions.append(auto_caption)
                        logger.info("FOUND: {},{}".format(caption_type, lang_code))

                else:
                    # collect the manual caption
                    captions.append(manual_caption)
                    logger.info("FOUND: {},{}".format(caption_type, lang_code))

        # return the list of captions
        return captions

    @classmethod
    def _dl_tracks(cls,
                   caption_comp_key: str,
                   caption_url: str) -> List[Track]:
        """
        this is where most of the errors occur.
        make sure to refactor this later in such a way that this is
        robust to all potential errors.
        :param caption_comp_key: the key of the caption.
        :param caption_url: the url to download the track from.
        :return: a list of Track objects
        """
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
        tracks = list()
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
                track = Track(track_comp_key, start, duration, text)
                tracks.append(track)
        return tracks



