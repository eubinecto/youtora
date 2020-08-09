from typing import List, Dict


class Channel:
    # for saving memory space
    __slots__ = (
        "channel_id",
        "url",
        "title",
        "subs",
        "lang_code",
        "vid_id_list",
    )

    def __init__(self,
                 channel_id: str,
                 uploader: str,
                 subs: int,
                 lang_code: str,
                 vid_id_list: list = None):
        """
        :param channel_id:
        :param uploader:
        :param vid_id_list: default is None (have a look at dl_playlist)
        """
        # key
        self.channel_id = channel_id

        self.url = "http://www.youtube.com/channel/{}"\
                            .format(channel_id)

        self.title = uploader

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
        'track_comp_key',
        'start',
        'duration',
        'content'
    )

    def __init__(self,
                 track_comp_key: str,
                 start: float,
                 duration: float,
                 content: str):
        # comp key
        self.track_comp_key = track_comp_key
        self.start = start
        self.duration = duration
        self.content = content

    # overrides dunder string method
    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.track_comp_key


class Caption:

    __slots__ = (
        'caption_comp_key',
        'is_auto',
        'lang_code',
        'url',
        'tracks'
    )

    def __init__(self,
                 caption_comp_key: str,
                 url: str,
                 tracks: List[Track]):
        """
        :param url: the url from which the tracks can be downloaded
        :param tracks: the list of tracks that belongs to this caption (1 to 1)
        """
        self.caption_comp_key = caption_comp_key
        self.is_auto = True if caption_comp_key.split("|")[1] == "auto" else False
        self.lang_code = caption_comp_key.split("|")[2]
        self.url = url
        # download the tracks on init of caption
        # list of track objects.
        self.tracks = tracks

    # overrides dunder string method
    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.caption_comp_key


class Video:

    # to save RAM space
    __slots__ = (
        'vid_id',
        'url',
        'title',
        'channel_id',
        'publish_date',
        'captions',
        'likes',
        'dislikes',
        'views'
    )

    def __init__(self,
                 vid_id: str,
                 title: str,
                 channel_id: str,
                 publish_date: str,
                 captions: Dict[str, Caption],
                 likes: int,
                 dislikes: int,
                 views: int):
        """
        :param vid_id: the unique id at the end of the vid url
        :param title: the title of the youtube video
        :param channel_id: the id of the channel this video belongs to
        :param publish_date: the uploaded date of the video
        :param captions: the dictionary of captions. keys are either auto or manual
        """
        # key
        self.vid_id = vid_id

        # build the url yourself... save the number of parameters.
        self.url = "https://www.youtube.com/watch?v={}"\
                        .format(vid_id)

        self.title = title
        self.channel_id = channel_id
        self.publish_date = publish_date
        self.captions = captions
        self.likes = likes
        self.dislikes = dislikes
        self.views = views

    # overrides the dunder string method
    def __str__(self):
        return self.title


# 이것도 재미있을 듯! <- 지금은 지금 해야하는 일에 집중.
# 어차피 개발 단계이므로, 계속 해나가면 된다.
class Chapter:
    pass
