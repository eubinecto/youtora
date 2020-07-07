from typing import List, Dict


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


class Track:

    __slots__ = '_track_comp_key', '_duration', '_text'

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


class Caption:

    __slots__ = '_caption_comp_key', '_caption_url', '_tracks'

    def __init__(self,
                 caption_comp_key: str,
                 caption_url: str,
                 tracks: List[Track]):
        """
        :param caption_comp_key:
        :param caption_url: the url from which the tracks can be downloaded
        :param tracks: the list of tracks that belongs to this caption (1 to 1)
        """
        # composite key
        self._caption_comp_key = caption_comp_key

        self._caption_url = caption_url

        # download the tracks on init of caption
        # list of track objects.
        self._tracks = tracks

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


class Video:

    # to save RAM space
    __slots__ = '_vid_id', '_vid_url', '_title', '_channel_id', '_upload_date', '_captions'

    def __init__(self,
                 vid_id: str,
                 title: str,
                 channel_id: str,
                 upload_date: str,
                 captions: Dict[str, Caption]):
        """
        :param vid_id: the unique id at the end of the vid url
        :param title: the title of the youtube video
        :param channel_id: the id of the channel this video belongs to
        :param upload_date: the uploaded date of the video
        :param captions: the dictionary of captions. keys are either auto or manual
        """
        # key
        self._vid_id = vid_id

        # build the url yourself... save the number of parameters.
        self._vid_url = "https://www.youtube.com/watch?v={}"\
                        .format(vid_id)

        self._title = title
        self._channel_id = channel_id
        self._upload_date = upload_date
        self._captions = captions

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
    def captions(self):
        return self._captions

    # overrides the dunder string method
    def __str__(self):
        return self._title


# 이것도 재미있을 듯!
class Chapter:
    pass
