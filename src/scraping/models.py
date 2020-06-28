

class Channel:
    def __init__(self,
                 channel_id: str,
                 uploader: str):
        # key
        self.channel_id = channel_id

        self.channel_url = "http://www.youtube.com/channel/{}"\
                            .format(channel_id)

        self.uploader = uploader
        # don't make foreign key links
        # So what is the reason for not making a foreign key link?
        # because if you do...Channel will get just so huge in size for
        # channels that have hundreds of videos.
        # so we need some degree of atomicity.
        # self.videos = videos

    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.uploader


class Video:
    def __init__(self,
                 vid_id: str,
                 title: str,
                 channel_id: str,
                 upload_date: str,
                 # what are their types?
                 subtitles,
                 automatic_captions):
        # key
        self.vid_id = vid_id

        # build the url yourself... save the number of parameters.
        self.vid_url = "https://www.youtube.com/watch?v={}"\
                        .format(vid_id)
        self.title = title
        self.channel_id = channel_id
        self.upload_date = upload_date

        # these two might be None.
        self.subtitles = subtitles
        self.automatic_captions = automatic_captions

    # overrides the dunder string method
    def __str__(self):
        return self.title


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
        :param vid_id: the video this caption belongs to.
        """
        # composite key
        self.caption_comp_key = "|".join([vid_id, caption_type, lang_code])

        self.caption_url = caption_url

    # overrides dunder string method
    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.caption_comp_key


class Track:
    def __init__(self,
                 caption_comp_key: str,
                 start, # so what are their types?
                 duration,
                 text: str):
        # comp key
        self.track_comp_key = "|".join([caption_comp_key, start])

        self.duration = duration
        self.text = text

    # overrides dunder string method
    def __str__(self) -> str:
        """
        overrides the dunder string method
        """
        return self.track_comp_key
