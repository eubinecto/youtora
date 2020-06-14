# the models that I'll be using.
from .models import Channel, Video, Caption, Track
#how do I use type alises?
import xmltodict

# for getting the xml caption
import requests

# use youtube_dl for getting the automatic captions
import youtube_dl


# if you give it a channel url, you can get a list of videos... hopefully?
class ChannelScraper:
    @classmethod
    def getChannel(cls, channel_url):
        """
        given a url, returns the metadata of the channel.
        :param url:
        :return: a Channel object.
        """
        pass


class VideoScraper:
    @classmethod
    def getVideo(cls, vid_url):
        """
        given a url, returns the meta data of the channel
        :param vid_url: the url of the video
        :return: a Video object
        """
        # get all of the captions, whether it be manual or auto.
        ydl_opts = {'writesubtitles': True,
                    'allsubtitles': True,
                    'writeautomaticsub': True}

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
        assert upload_date is not None, "upload_date is required"

        # returns a video object with the properites above
        return Video(vid_id,
                     title,
                     channel_id,
                     upload_date,
                     subtitles,
                     automatic_captions)

    @classmethod
    def extractVideos(cls, channel):
        """
        :param channel: given a Channel Object
        :return: returns Videos (a list of Video objects)
        """
        # type check
        isinstance(channel, Channel)
        pass


class CaptionScraper:
    # the cpation types defined
    CAPTION_TYPES = ["manual", "auto"]

    # list of caption formats
    CAPTION_FORMATS = {'srv1': 0,
                       'srv2': 1,
                       'srv3': 2,
                       'ttml': 3,
                       'vtt': 4}

    # the caption format I'll be using
    CAPTION_FORMAT = 'srv1'

    @classmethod
    def getCaption(cls,
                   vid_url,
                   lang_code='en',
                   caption_type=None):
        """
        downlaod a caption from the video url directly
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
    def extractCaption(cls,
                       video,
                       lang_code='en',
                       caption_type=None):
        """
        extract the caption from a given video object
        instead of downlaoding it directly from a vid_url.
        :param video: a video object
        :param lang_code: the desired langauge
        :param caption_type: None: any , manual: manually written, auto: auto caption
        :return: a caption object
        """
        # type check - must be a video object
        isinstance(video, Video)
        # input check - must be either None, "auto", "manual"
        assert caption_type in ([None] + cls.CAPTION_TYPES), "invalid caption Type:{}" \
            .format(caption_type)

        # check for the existance of the captions for both types
        manual_exists = lang_code in video.subtitles
        auto_exists = lang_code in video.automatic_captions

        vid_id = video.vid_id
        caption_url = None

        #prioritise manual
        if caption_type is None:
            if manual_exists:
                caption_type = "manual"
                caption_url = video.subtitles[lang_code]\
                                             [cls.CAPTION_FORMATS[cls.CAPTION_FORMAT]]\
                                             ['url']
            #if manual caption does not exist, get the automatic one
            elif auto_exists:
                caption_type = "auto"
                caption_url = video.automatic_captions[lang_code]\
                                                      [cls.CAPTION_FORMATS[cls.CAPTION_FORMAT]]\
                                                      ['url']
        elif caption_type == "manual":
            if manual_exists:
                caption_url = video.subtitles[lang_code]\
                                             [cls.CAPTION_FORMATS[cls.CAPTION_FORMAT]]\
                                             ['url']
        elif caption_type == "auto":
            if auto_exists:
                caption_url = video.automatic_captions[lang_code]\
                                                      [cls.CAPTION_FORMATS[cls.CAPTION_FORMAT]]\
                                                      ['url']

        if caption_url is None:
            # raise an exception if no caption was found
            raise KeyError("NOT FOUND:{}:lang_code={}:vid={}" \
                           .format(caption_type if caption_type is not None else "manual&auto",
                                   lang_code,
                                   video))

        return Caption(vid_id=vid_id,
                       caption_type=caption_type,
                       lang_code=lang_code,
                       caption_url=caption_url)

    @classmethod
    def getTracks(cls, caption):
        """
        :param caption: a caption Object with caption url
        :return: a list of Track objects
        """
        isinstance(caption, Caption)
        #first, get the xml

        tracksXML = requests.get(caption.caption_url).content
        #deserialse the xml to dict
        tracksDict = xmltodict.parse(tracksXML)

        #the composite key of the caption
        caption_comp_key = "|".join([caption.vid_id, caption.caption_type, caption.lang_code])
        tracks = list()
        for trackItem in tracksDict['transcript']['text']:
            start = trackItem["@start"]
            duration = trackItem["@dur"]
            text = trackItem["#text"]
            track = Track(caption_comp_key, start, duration, text)
            tracks.append(track)

        return tracks



