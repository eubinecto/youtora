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

        # returns a video object with the properties above
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
        # will I need this in the first place?
        pass

    @classmethod
    def get_tracks(cls, caption: Caption) -> List[Track]:
        """
        :param caption: a caption Object with caption url
        :return: a list of Track objects
        """
        #error handling
        if not isinstance(caption, Caption):
            raise TypeError

        # first, get the response
        response = requests.get(caption.caption_url)

        # check if the response was erroneous
        response.raise_for_status()

        # if the request was successful, get the xml
        tracks_xml = response.content

        # deserialize the xml to dict
        tracks_dict = xmltodict.parse(tracks_xml)

        # the composite key of the caption
        caption_comp_key = caption.caption_comp_key

        # prepare a bucket for tracks
        tracks = list()

        # get the tracks
        for trackItem in tracks_dict['transcript']['text']:
            start = trackItem["@start"]
            duration = trackItem["@dur"]
            text = trackItem["#text"]
            track = Track(caption_comp_key, start, duration, text)
            tracks.append(track)

        return tracks
