from typing import List


class YouTubeModel:
    def __init__(self):
        self.id = None
        self.parent_id = None

    pass


class Channel(YouTubeModel):
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
        super().__init__()
        # key
        self.id = channel_id

        self.url = "http://www.youtube.com/channel/{}"\
                            .format(channel_id)

        self.title = title

        # social feature
        self.subs = subs

        # the lang code of the channel the code will be manually given
        self.lang_code = lang_code

        # no reference to actual video objects
        # just reference video id's here. (in case there are too many videos to download)
        self.vid_id_list = vid_id_list

    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.title


class Track(YouTubeModel):
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
        super().__init__()

        # comp key
        self.id = track_id
        self.parent_id = caption_id
        self.start = start
        self.duration = duration
        self.content = content
        self.text_area_rel_img = None

    def set_text_area_rel_img(self, text_area_rel_img: float):
        self.text_area_rel_img: float = text_area_rel_img

    # overrides dunder string method
    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.id


class Caption(YouTubeModel):

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
                 url: str):
        """
        :param url: the url from which the tracks can be downloaded
        """
        super().__init__()

        self.id = caption_id
        self.parent_id = vid_id
        self.is_auto = True if caption_id.split("|")[1] == "auto" else False
        self.lang_code = caption_id.split("|")[2]
        self.url = url
        self.tracks = None

    # setter method
    def set_tracks(self, tracks: List[Track]):
        self.tracks: List[Track] = tracks

    # overrides dunder string method
    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.id


class Video(YouTubeModel):
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

    def __init__(self,
                 vid_id: str,
                 channel_id: str,
                 title: str,
                 publish_date: str,
                 likes: int,
                 dislikes: int,
                 views: int,
                 category: str,
                 manual_sub_info: dict,
                 auto_sub_info: dict):
        """
        :param vid_id: the unique id at the end of the vid url
        :param title: the title of the youtube video
        :param channel_id: the id of the channel this video belongs to
        :param publish_date: the uploaded date of the video
        """
        super().__init__()

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
        self.manual_sub_info = manual_sub_info
        self.auto_sub_info = auto_sub_info
        self.captions = None

    def set_captions(self, captions: List[Caption]):
        self.captions: List[Caption] = captions

    # overrides the dunder string method
    def __str__(self) -> str:
        return self.title


class Frame(YouTubeModel):

    __slots__ = (
        "id",
        "parent_id",
        "time_stamp"
    )

    def __init__(self,
                 frame_id: str,
                 vid_id: str,
                 time_stamp: int):
        """
        :param frame_id:
        :param vid_id:
        :param time_stamp: the should be an integer.
        """

        super().__init__()
        self.id = frame_id
        self.parent_id = vid_id
        self.time_stamp = time_stamp


# 이것도 재미있을 듯! <- 지금은 지금 해야하는 일에 집중.
# 어차피 개발 단계이므로, 계속 해나가면 된다.
class Chapter(YouTubeModel):
    pass
