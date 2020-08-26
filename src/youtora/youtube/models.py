import html
import logging
import requests
from typing import List

import xmltodict

from src.youtora.youtube.errors import CaptionNotFoundError


class Channel:
    # for saving memory space
    __slots__ = (
        "id",
        "url",
        "title",
        "subs",
        "lang_code",
        "vid_id_list",
    )

    def __init__(self,
                 channel_id: str,
                 title: str,
                 subs: int,
                 lang_code: str,
                 vid_id_list: list = None):
        """
        :param channel_id:
        :param title:
        :param vid_id_list: default is None (have a look at dl_playlist)
        """
        # key
        self.id = channel_id

        self.url = "http://www.youtube.com/channel/{}"\
                            .format(channel_id)

        self.title = title

        # social feature
        self.subs = subs

        # the lang code of the channel
        # the code will be manually given
        self.lang_code = lang_code

        # no reference to actual video objects
        # just reference video id's here. (in case there are too many videos to download)
        self.vid_id_list = vid_id_list

    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.title


class Track:
    __slots__ = (
        'id',
        'parent_id',
        'start',
        'duration',
        'content'
    )

    def __init__(self,
                 track_id: str,
                 caption_id: str,
                 start: float,
                 duration: float,
                 content: str):
        # comp key
        self.id = track_id
        self.parent_id = caption_id
        self.start = start
        self.duration = duration
        self.content = content

    # overrides dunder string method
    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.id


class Caption:

    __slots__ = (
        'id',
        'parent_id',
        'is_auto',
        'lang_code',
        'url',
        'tracks',
    )

    def __init__(self,
                 caption_id: str,
                 vid_id: str,
                 url: str,
                 tracks: List[Track] = None):
        """
        :param url: the url from which the tracks can be downloaded
        """
        self.id = caption_id
        self.parent_id = vid_id
        self.is_auto = True if caption_id.split("|")[1] == "auto" else False
        self.lang_code = caption_id.split("|")[2]
        self.url = url
        # list of track objects.
        if tracks:
            self.tracks = tracks
        else:
            self.tracks: List[Track] = list()

    def dl_tracks(self):
        if self.tracks:
            raise ValueError("tracks have already been downloaded")

        logger = logging.getLogger("dl_tracks")
        # first, get the response (download)
        response = requests.get(self.url)
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
            track_comp_key = "|".join([self.id, '0'])
            # append to the tracks
            self.tracks.append(Track(track_id=track_comp_key,
                                     caption_id=self.id,
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
                track_comp_key = "|".join([self.id, str(idx)])

                # append to the tracks
                self.tracks.append(Track(track_id=track_comp_key,
                                         caption_id=self.id,
                                         start=start,
                                         duration=duration,
                                         content=text))

    # overrides dunder string method
    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.id


class Video:
    # to save RAM space
    __slots__ = (
        'id',
        'parent_id',
        'url',
        'title',
        'publish_date',
        'likes',
        'dislikes',
        'views',
        'category',
        'manual_sub_info',
        'auto_sub_info',
        'captions',
    )

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

    def __init__(self,
                 vid_id: str,
                 channel_id: str,
                 title: str,
                 publish_date: str,
                 likes: int,
                 dislikes: int,
                 views: int,
                 category: str,
                 captions: List[Caption] = None,
                 manual_sub_info: dict = None,
                 auto_sub_info: dict = None):
        """
        :param vid_id: the unique id at the end of the vid url
        :param title: the title of the youtube video
        :param channel_id: the id of the channel this video belongs to
        :param publish_date: the uploaded date of the video
        """
        # key
        self.id = vid_id

        # build the url yourself... save the number of parameters.
        self.url = "https://www.youtube.com/watch?v={}"\
                        .format(vid_id)

        self.title = title
        self.parent_id = channel_id
        self.publish_date = publish_date
        self.likes = likes
        self.dislikes = dislikes
        self.views = views
        self.category = category
        # init as an empty list
        if captions:
            # captions are explicitly given
            self.captions = captions
        else:
            if manual_sub_info or auto_sub_info:
                self.manual_sub_info = manual_sub_info
                self.auto_sub_info = auto_sub_info
                self.captions: List[Caption] = list()
                # add captions on init
                self.add_captions()
            else:
                raise ValueError("one of the info must be given")

    def _add_caption(self,
                     caption_type: str,
                     lang_code: str):
        """
        extract the caption from the video object
        need to handle the case where the lang code does not exist.
        I think you might need to download the list of lang codes.
        :param caption_type: manual = manually written, auto = ASR. the default is auto.
        :param lang_code: the language code should be given
        :return: a caption object
        """

        # input check - must be either  "manual" or "auto"
        if caption_type not in self.CAPTION_TYPES:
            raise ValueError(caption_type)

        # set the desired caption format in the CaptionScraper class.
        format_idx = self.FORMAT_IDX[self.CAPTION_FORMAT]

        # this is initially None
        caption_url = None

        # switch statement
        if caption_type == "manual":
            if lang_code in self.manual_sub_info:  # manual exists
                caption_url = self.manual_sub_info[lang_code][format_idx]['url']
        elif caption_type == "auto":  # auto exists
            if lang_code in self.auto_sub_info:
                caption_url = self.auto_sub_info[lang_code][format_idx]['url']

        # Note: a None is a singleton object.
        # there can only be 1 None.
        # So whatever variable that is assigned to None keyword
        # refers to the same memory location. ("NULL" in C)
        # so it makes sense to use is operator rather than equality operator.
        if not caption_url:
            raise CaptionNotFoundError("NOT FOUND: {},{}"
                                       .format(caption_type, lang_code))

        # this will be the id of each caption
        caption_comp_key = "|".join([self.id, caption_type, lang_code])

        # return the caption object with tracks
        caption = Caption(caption_id=caption_comp_key,
                          vid_id=self.id,
                          url=caption_url)

        # append to the caption list
        self.captions.append(caption)

    def add_captions(self):
        """
        given a list of videos, downloads all captions for each video.
        """
        logger = logging.getLogger("dl_captions")

        # captions now should be a list of captions
        captions = list()

        # loop through all of the videos.
        for lang_code in self.LANG_CODES_TO_COLLECT:
            try:
                # manual
                # first get all available manual captions.
                caption_type = "manual"
                manual_caption = self._add_caption(caption_type=caption_type,
                                                   lang_code=lang_code)
            except CaptionNotFoundError as ce:
                # try getting an automatic one
                try:
                    caption_type = "auto"
                    auto_caption = self._add_caption(caption_type=caption_type,
                                                     lang_code=lang_code)
                except CaptionNotFoundError as ce:
                    # automatic one was not found either
                    logger.warning("NOT FOUND: manual & auto:" + lang_code)
                else:
                    # collect the automatic caption
                    captions.append(auto_caption)
            else:
                # collect the manual caption
                captions.append(manual_caption)

    # overrides the dunder string method
    def __str__(self):
        return self.title


# 이것도 재미있을 듯! <- 지금은 지금 해야하는 일에 집중.
# 어차피 개발 단계이므로, 계속 해나가면 된다.
class Chapter:
    pass
