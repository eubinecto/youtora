class Channel:
    def __init__(self,
                 channel_id,
                 uploader):
        """
        :param channel_url:
        :param uploader:
        :param videos: list of Video objects
        """
        #-----------------
        self.channel_id = channel_id
        #----------------- primary key

        self.channel_url = "http://www.youtube.com/channel/{}"\
                            .format(channel_id)

        self.uploader = uploader
        #don't make foriegn key links
        #self.videos = videos

    def __str__(self):
        return self.uploader


class Video:
    def __init__(self,
                 vid_id,
                 title,
                 channel_id,
                 upload_date,
                 subtitles,
                 automatic_captions):
        #-----------------
        self.vid_id = vid_id
        #----------------- primary key

        #build the url yourself... save the number of paramters.
        self.vid_url = "https://www.youtube.com/watch?v={}"\
                        .format(vid_id)
        self.title = title
        self.channel_id = channel_id
        self.upload_date = upload_date #this

        #these two might be None.
        self.subtitles = subtitles
        self.automatic_captions = automatic_captions


    #toString method.
    def __str__(self):
        return self.title



class Caption:
    def __init__(self,
                 vid_id,
                 caption_type,
                 lang_code,
                 caption_url):
        """
        :param caption_id: the unique id found in the url
        :param caption_type: manual / auto
        :param lang_code: en, kr , etc
        :param vid_id: the video this caption belongs to.
        """
        #---------------
        self.vid_id = vid_id
        self.caption_type = caption_type
        self.lang_code = lang_code
        #--------------- comp key

        self.caption_url = caption_url


    def __str__(self):
        return ":".join([self.vid_id, self.caption_type, self.lang_code])

class Track:
    def __init__(self,
                 caption_comp_key,
                 start,
                 duration,
                 text):
        #-----------------
        self.caption_comp_key = caption_comp_key
        self.start = start
        #----------------- composite key
        self.duration = duration
        self.text = text


    def __str__(self):
        return ":".join([self.vid_id, self.start, self.text])

