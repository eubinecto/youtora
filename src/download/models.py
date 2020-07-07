from typing import List

from .downloaders import TrackDownloader


class Channel:
    def __init__(self,
                 channel_id: str,
                 uploader: str,
                 playlist):
        # key
        self._channel_id = channel_id

        self._channel_url = "http://www.youtube.com/channel/{}"\
                            .format(channel_id)

        self._uploader = uploader
        # don't make foreign key links
        # So what is the reason for not making a foreign key link?
        # because if you do...Channel will get just so huge in size for
        # channels that have hundreds of videos.
        # so we need some degree of atomicity.
        # self.videos = videos <- not including this.
        self._playlist = playlist

    # accessor methods
    # property decorator allows you to
    # access protected variable by just using the name of
    # the method.
    @property
    def channel_id(self):
        return self._channel_id

    @property
    def channel_url(self):
        return self._channel_url

    @property
    def playlist(self):
        return self._playlist

    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self._uploader


class Video:
    def __init__(self,
                 vid_id: str,
                 title: str,
                 channel_id: str,
                 upload_date: str,
                 # what are their types?
                 subtitles,
                 auto_captions):
        # key
        self._vid_id = vid_id

        # build the url yourself... save the number of parameters.
        self._vid_url = "https://www.youtube.com/watch?v={}"\
                        .format(vid_id)

        self._title = title
        self._channel_id = channel_id
        self._upload_date = upload_date

        # these two might be None.
        self._subtitles = subtitles
        self._auto_captions = auto_captions

    # accessor methods
    @property
    def vid_id(self):
        return self._vid_id

    @property
    def vid_url(self):
        return self._vid_url

    @property
    def title(self):
        return self._title

    @property
    def channel_id(self):
        return self._channel_id

    @property
    def upload_date(self):
        return self._upload_date

    @property
    def subtitles(self):
        return self._subtitles

    @property
    def auto_captions(self):
        return self._auto_captions

    # overrides the dunder string method
    def __str__(self):
        return self._title


class Caption:
    def __init__(self,
                 vid_id: str,
                 caption_type: str,
                 lang_code: str,
                 caption_url: str):
        """
        :param vid_id: the unique id of the video.
        :param caption_type: manual / auto
        :param lang_code: en, kr , etc
        :param caption_url: the url from which the tracks can be downloaded
        """
        # composite key
        self._caption_comp_key = "|".join([vid_id, caption_type, lang_code])

        self._caption_url = caption_url

        # download the tracks on init of caption
        # list of track objects.
        self._tracks: List[Track] = TrackDownloader.dl_tracks(caption_comp_key=self._caption_comp_key,
                                                              caption_url=self._caption_url)

    # accessor methods
    @property
    def caption_comp_key(self):
        return self._caption_comp_key

    @property
    def caption_url(self):
        return self._caption_url

    @property
    def tracks(self):
        return self._tracks

    # overrides dunder string method
    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self._caption_comp_key


class Track:
    def __init__(self,
                 caption_comp_key: str,
                 start,
                 duration,
                 text: str):
        # comp key
        self._track_comp_key = "|".join([caption_comp_key, start])

        self._duration = duration
        self._text = text

    # accessor methods
    @property
    def track_comp_key(self):
        return self._track_comp_key

    @property
    def duration(self):
        return self._duration

    @property
    def text(self):
        return self._text

    # overrides dunder string method
    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self._track_comp_key
