# the models that I'll be using.
from typing import List

from .models import Channel, Video, Caption, Track
# how do I use type aliases?
import xmltodict

# for getting the xml caption from timed text api.
import requests

# use youtube_dl for getting the automatic captions
import youtube_dl


# if you give it a channel url, you can get a list of videos... hopefully?
class ChannelScraper:

    @classmethod
    def get_channel(cls, channel_url: str) -> Channel:
        pass


class VideoScraper:

    @classmethod
    def extract_videos(cls, channel: Channel):
        """
        :param channel: given a Channel Object
        :return: returns Videos (a list of Video objects)
        """
        # type check
        if not isinstance(channel, Channel):
            raise TypeError

        pass

    @classmethod
    def get_video(cls, vid_url: str) -> Video:
        """
        given a url, returns the meta data of the channel
        :param vid_url: the url of the video
        :return: a Video object
        """
        # get all of the captions, whether it be manual or auto.
        ydl_opts = {'writesubtitles': True,
                    'allsubtitles': True,
                    'writeautomaticsub': True}

        # get the info.
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url=vid_url, download=False)

        # access the results
        vid_id = info['id']
        title = info['title']
        channel_id = info['channel_url']
        upload_date = info['upload_date']
        subtitles = info['subtitles']
        automatic_captions = info['automatic_captions']

        # asserting: these four must not be None
        assert vid_id is not None, "vid_id is required"
        assert title is not None, "title is required"
        assert channel_id is not None, "channel_id is required"
        # I might need upload date to sort by recency.
        assert upload_date is not None, "upload_date is required"

        # returns a video object with the properites above
        return Video(vid_id,
                     title,
                     channel_id,
                     upload_date,
                     subtitles,
                     automatic_captions)


class CaptionScraper:
    # the caption types defined
    CAPTION_TYPES = ("manual", "auto")

    # list of caption formats
    FORMAT_IDX = {
        'srv1': 0,
        'srv2': 1,
        'srv3': 2,
        'ttml': 3,
        'vtt': 4
    }

    # the caption format I'll be using
    CAPTION_FORMAT = 'srv1'

    @classmethod
    def extract_caption(cls,
                        video: Video,
                        lang_code: str = 'en',
                        caption_type: str = "auto"):
        """
        extract the caption from a given video object
        instead of downloading it directly from a vid_url.
        :param video: a video object
        :param lang_code: the desired language
        :param caption_type:manual: manually written, auto: ASR. the default is auto.
        :return: a caption object
        """
        # type check - must be a video object
        if not isinstance(video, Video):
            raise TypeError(video)

        # input check - must be either None, "auto", "manual"
        if caption_type not in cls.CAPTION_TYPES:
            raise ValueError(caption_type)

        # check for the existence of the captions for both types
        manual_exists = lang_code in video.subtitles
        auto_exists = lang_code in video.auto_captions()

        vid_id = video.vid_id()
        format_idx = cls.FORMAT_IDX[cls.CAPTION_FORMAT]
        caption_url = None

        if caption_type == "manual":
            if manual_exists:
                caption_url = video.subtitles()[lang_code][format_idx]['url']
        elif caption_type == "auto":
            if auto_exists:
                caption_url = video.auto_captions()[lang_code][format_idx]['url']

        # to be handled
        # Note: a None is a singleton object.
        # there can only be 1 None.
        # So whatever variable that is assigned to None keyword
        # refers to the same memory location. ("NULL" in C)
        # so it makes sense to use is operator rather than equality operator.
        if caption_type is None:
            raise ValueError(caption_type)

        return Caption(vid_id=vid_id,
                       caption_type=caption_type,
                       lang_code=lang_code,
                       caption_url=caption_url)

    @classmethod
    def get_caption(cls,
                    vid_url: str,
                    lang_code: str = 'en',
                    caption_type: str = "auto"):
        """
        download a caption from the video url directly
        :param vid_url: the vid url to get the caption from.
        :param lang_code: the desired language you want the caption to be written in.
        :param caption_type: either manual / auto. if None, it type manual is prioritised.
        :return: a Caption object
        """
        # first, write code for handling errors in the script.
        # esp
        pass
        # use if key in dict to check if the caption with the language code exists

    @classmethod
    def get_tracks(cls, caption: Caption) -> List[Track]:
        """
        :param caption: a caption Object with caption url
        :return: a list of Track objects
        """
        if not isinstance(caption, Caption):
            raise TypeError
        # first, get the xml

        tracks_xml = requests.get(caption.caption_url).content
        # deserialize the xml to dict
        tracks_dict = xmltodict.parse(tracks_xml)

        # the composite key of the caption
        caption_comp_key = caption.caption_comp_key()
        tracks = list()
        for trackItem in tracks_dict['transcript']['text']:
            start = trackItem["@start"]
            duration = trackItem["@dur"]
            text = trackItem["#text"]
            track = Track(caption_comp_key, start, duration, text)
            tracks.append(track)

        return tracks
