
# import all the models needed
from .models import (
    ChannelRaw,
    CaptionsRaw,
    TracksRaw,
    VideoRaw, MLGloss, MLGlossDesc
)
from .dataclasses import (
    ChannelData,
    VideoData,
    TrackData,
    CaptionData
)
from .scrapers import TracksRawScraper, MLGlossHTMLScraper
from typing import List, Tuple, Generator, Collection
import logging
import requests
import re
import html
import xmltodict
# for parsing
from bs4 import BeautifulSoup
from .errors import CaptionNotFoundError


class ChannelRawParser:
    # XPaths for the elements that we want to access
    # inspect these from chrome browser
    SUB_CNT_CLASS = "c4-tabbed-header-subscriber-count"  # get rid of th empty space
    UPLOADED_THUMB_CLASS = "compact-media-item-image"

    @classmethod
    def parse(cls, channel_raw: ChannelRaw) -> ChannelData:
        # parse the main html's to get the title and subs.
        title = cls._ext_title(channel_raw.main_html)
        subs = cls._ext_subs(channel_raw.main_html)
        # parse uploads html to get the list of all uploaded videos
        vid_id_list = cls._ext_video_id_list(channel_raw.uploads_html)
        # the channel_raw is given a lang code
        return ChannelData(id=channel_raw.id,
                           url=channel_raw.url,
                           lang_code=channel_raw.lang_code,
                           title=title,
                           subs=subs,
                           vid_id_list=vid_id_list)

    @classmethod
    def _ext_title(cls, main_html: str) -> str:
        """
        e.g.
        <title>Abdul Bari - YouTube</title>
        """
        soup = BeautifulSoup(main_html, 'html.parser')
        title_elem = soup.find('title')
        return title_elem.text.split("-")[0].strip()

    @classmethod
    def _ext_subs(cls, main_html: str) -> int:
        """
        keep in mind that the subs count is
        only a rough value.
        e.g.
        <span class="c4-tabbed-header-subscriber-count secondary-text">285K subscribers</span>
        :return: the approximate sub count of the channel_raw
        """
        soup = BeautifulSoup(main_html, 'html.parser')
        span_elem = soup.find('span', attrs={'class': cls.SUB_CNT_CLASS})
        # get the data
        span_data = span_elem.text.split(" ")[0].strip()
        # Now I have to parse this
        if re.match(r'[\d.]*[KMB]$', span_data):
            if span_data[-1] == 'K':
                subs_cnt = int(float(span_data[:-1]) * (10 ** 3))
            elif span_data[-1] == 'M':
                subs_cnt = int(float(span_data[:-1]) * (10 ** 6))
            else:
                # has a billion subs
                subs_cnt = int(float(span_data[:-1]) * (10 ** 9))
        else:
            # less than 1K
            subs_cnt = int(span_data)
        # check the value for debugging
        return subs_cnt

    @classmethod
    def _ext_video_id_list(cls, uploads_html: str) -> List[str]:
        # get all the elements that are of this class
        soup = BeautifulSoup(uploads_html, 'html.parser')
        video_id_list = list()
        # is this div tag?
        uploaded_thumbs = soup.find_all('a', attrs={'class': cls.UPLOADED_THUMB_CLASS})
        for thumb in uploaded_thumbs:
            # get the href attribute,
            thumb_url = thumb['href']
            video_id = thumb_url.split("=")[-1].strip()
            video_id_list.append(video_id)
        # now get the boxes.
        # when everything is done
        # collect the video ids.
        return video_id_list


class CaptionsRawParser:
    # manually written captions, asr caption
    CAPTION_TYPES = ("manual", "auto")
    # the caption format I'll be using
    CAPTION_FORMAT = 'srv1'
    # list of caption formats used by youtube_dl
    FORMATS = {
        'srv1': 0,
        'srv2': 1,
        'srv3': 2,
        'ttml': 3,
        'vtt': 4
    }
    # the format index to use
    FORMAT_IDX = FORMATS[CAPTION_FORMAT]
    # korean, japanese, english, british english, french
    # we are only downloading captions of these languages .
    # these are the languages of the captions that I'll be collecting
    # (actual value, human readable name) tuples.
    LANG_CODES_TO_COLLECT = (
        ('ko', 'korean'),
        ('ja', 'japanese'),
        ('en', 'english'),
        ('en-GB', 'british english'),
        ('fr', 'french')
    )

    @classmethod
    def parse(cls, captions_raw: CaptionsRaw) -> List[CaptionData]:
        logger = logging.getLogger("parse")
        # as for json field, you must use getattr
        auto_info: dict = getattr(captions_raw, captions_raw.auto_captions_info.column)
        manual_info: dict = getattr(captions_raw, captions_raw.manual_captions_info.column)
        video_id = captions_raw.video_id
        captions = list()
        # loop through all the lang codes
        for lang_code, _ in cls.LANG_CODES_TO_COLLECT:
            try:  # try getting manual captions first
                manual_caption = cls._ext_caption(manual_info, video_id,
                                                  cls.CAPTION_TYPES[0],
                                                  lang_code)
            except CaptionNotFoundError:
                try:  # if that didn't work, try getting auto caption
                    auto_caption = cls._ext_caption(auto_info, video_id,
                                                    cls.CAPTION_TYPES[1],
                                                    lang_code)
                except CaptionNotFoundError:  # automatic one was not found either
                    logger.warning("NOT FOUND: manual & auto:" + lang_code)
                else:  # collect the automatic caption found
                    captions.append(auto_caption)
            else:  # collect the manual caption found
                captions.append(manual_caption)
        # return captions. this could be empty.
        return captions

    @classmethod
    def parse_multi(cls, captions_raw_list: List[CaptionsRaw]) -> List[CaptionData]:
        # flatten to list of captions
        return [
            caption
            for captions_raw in captions_raw_list
            for caption in cls.parse(captions_raw)
        ]

    @classmethod
    def _ext_caption(cls, caption_info: dict,
                          video_id: str,
                          caption_type: str,
                          lang_code: str) -> CaptionData:
        # input check - must be either  "manual" or "auto"
        if caption_type not in cls.CAPTION_TYPES:
            raise ValueError(caption_type)
        # this is initially None
        caption_url = None
        if lang_code in caption_info.keys():  # manual exists
            caption_url = caption_info[lang_code][cls.FORMAT_IDX]['url']
        if not caption_url:
            raise CaptionNotFoundError("NOT FOUND: {},{}"
                                       .format(caption_type, lang_code))
        # this will be the id of each caption
        caption_id = "|".join([video_id, caption_type, lang_code])
        # return the caption object with tracks
        caption = CaptionData(id=caption_id,
                              video_id=video_id,
                              is_auto=True if caption_type == "auto" else False,
                              lang_code=lang_code,
                              url=caption_url)
        # scrape the tracks for this caption
        tracks_raw = TracksRawScraper.scrape(caption)
        # parse it and set tracks
        cls._ext_and_set_tracks(tracks_raw, caption)
        return caption

    @classmethod
    def _ext_and_set_tracks(cls, tracks_raw: TracksRaw, caption: CaptionData):
        # download the tracks
        tracks = TracksRawParser.parse(tracks_raw)
        caption.set_tracks(tracks)


class TracksRawParser:
    @classmethod
    def parse(cls, tracks_raw: TracksRaw) -> List[TrackData]:
        logger = logging.getLogger("parse")
        tracks = list()
        tracks_caption_id = tracks_raw.caption_id
        tracks_xml = html.unescape(tracks_raw.xml.__str__())
        tracks_dict = xmltodict.parse(tracks_xml)  # deserialize the xml to dict
        # if not a  list, ignore. quirk of youtube_dl - if there is only one track,
        # then the value of text is a dict, not a list.
        # e.g. https://www.youtube.com/watch?v=1SMmc9gQmHQ
        if isinstance(tracks_dict['transcript']['text'], list):
            for trackItem in tracks_dict['transcript']['text']:
                try:
                    start: float = float(trackItem["@start"])
                    duration: float = float(trackItem["@dur"])
                    content = trackItem["#text"]
                except KeyError as ke:
                    # if either one of them does not exist,then just skip this track
                    # as it is not worthy of storing
                    logger.warning("SKIP: track does not have:" + str(ke))
                    continue
                else:
                    # build track and collect
                    track = TrackData(caption_id=tracks_caption_id,
                                      start=start,
                                      duration=duration,
                                      content=content)
                    tracks.append(track)
        # set these and return
        cls._set_neighbours(tracks)
        cls._set_contexts(tracks)
        return tracks

    @classmethod
    def _set_neighbours(cls, tracks: List[TrackData]):
        """
        sets the prev_id & next_id of all the tracks in the list
        """
        for idx, track in enumerate(tracks):
            if idx == 0:
                # the first track has no prev_id; it only has next_id
                prev_id = None
                next_id = tracks[idx + 1].id
            elif idx == (len(tracks) - 1):
                # the last track has no next_id; it only has prev_id
                prev_id = tracks[idx - 1].id
                next_id = None
            else:
                # middle tracks have both prev_id and next_id
                prev_id = tracks[idx - 1].id
                next_id = tracks[idx + 1].id
            # set prev & next
            track.prev_id = prev_id
            track.next_id = next_id

    @classmethod
    def _set_contexts(cls, tracks: List[TrackData]):
        for idx, track in enumerate(tracks):
            # get the current id
            curr_content = track.content
            if idx == 0:
                prev_content = ""
                next_content = tracks[idx + 1].content
            elif idx == (len(tracks) - 1):
                prev_content = tracks[idx - 1].content
                next_content = ""
            else:
                prev_content = tracks[idx - 1].content
                next_content = tracks[idx + 1].content
            # set the context
            track.context = " ".join([prev_content, curr_content, next_content])


class VideoRawParser:
    VID_URL_FORMAT = "https://www.youtube.com/watch?v={}"

    HEADERS = {
        # get the english page
        "Accept-Language": "en"
    }

    @classmethod
    def parse(cls, video_raw: VideoRaw) -> VideoData:
        info: dict = video_raw.video_info
        # access the results
        vid_id = info['id']
        title = info['title']
        upload_date = "{year}-{month}-{day}" \
            .format(year=info['upload_date'][:4],
                    month=info['upload_date'][4:6],
                    day=info['upload_date'][6:])  # e.g. 20200610 -> 2020-06-10
        views = info['view_count']
        # the length is always greater than zero;  use the first one as the category of this video
        category = info['categories'][0]
        manual_info: dict = getattr(video_raw.captions_raw,
                                    video_raw.captions_raw.manual_captions_info.column)
        auto_info: dict = getattr(video_raw.captions_raw,
                                  video_raw.captions_raw.auto_captions_info.column)
        channel_id = video_raw.channel_raw.id
        vid_url = cls.VID_URL_FORMAT.format(vid_id)
        # better collect these info separately
        likes, dislikes = cls._ext_likes_dislikes(vid_url)
        # creates a video object
        video = VideoData(id=vid_id, title=title, url=vid_url,
                          channel_id=channel_id, publish_date=upload_date,
                          likes=likes, dislikes=dislikes, views=views,
                          category=category, manual_captions_info=manual_info,
                          auto_captions_info=auto_info)
        # set captions and tracks
        cls._ext_and_set_captions(video_raw.captions_raw, video)
        return video

    @classmethod
    def parse_multi(cls, video_raw_coll: Collection[VideoRaw]) -> Generator[VideoData, None, None]:
        return (
            cls.parse(video_raw)
            for video_raw in video_raw_coll
        )

    @classmethod
    def _ext_likes_dislikes(cls, vid_url) -> Tuple[int, int]:
        """
        must collect them together because
        """
        # get the page
        html_text = requests.get(url=vid_url, headers=cls.HEADERS).text
        # the first will be like info, the latter will be dislike info
        results = re.findall(r'"toggleButtonRenderer":{.*?"accessibilityData":{"label":"(.*?)"}}', html_text)
        # search for like counts
        like_info = results[0].strip()
        dislike_info = results[1].strip()
        if like_info == "I like this" and dislike_info == "I dislike this":
            # like count and dislike count does not exist
            # which means their values are zero.
            like_cnt = 0
            dislike_cnt = 0
            logging.info("no likes & dislikes for video:" + vid_url)
        else:
            like_cnt_info = like_info.split(" ")[0].strip()
            dislike_cnt_info = dislike_info.split(" ")[0].strip()
            # get the like cnt
            if like_cnt_info == "No":
                like_cnt = 0
                logging.info("like_cnt:0:video:" + vid_url)
            else:
                like_cnt = int(like_cnt_info.replace(",", ""))
                logging.info("like_cnt:{}:video:{}".format(like_cnt, vid_url))
            # get the dislike cnt
            if dislike_cnt_info == "No":
                dislike_cnt = 0
                logging.info("dislike_cnt:0:video:" + vid_url)
            else:
                dislike_cnt = int(dislike_cnt_info.replace(",", ""))
                logging.info("dislike_cnt:{}:video:{}".format(dislike_cnt, vid_url))
        return like_cnt, dislike_cnt

    @classmethod
    def _ext_and_set_captions(cls, captions_raw: CaptionsRaw, video: VideoData):
        captions = CaptionsRawParser.parse(captions_raw)
        video.set_captions(captions)


class MLGlossHTMLParser:
    """
    houses logic for parsing raw MLGloss
    """
    # urls
    IMAGES_URL: str = "https://developers.google.com/machine-learning/glossary/images/"
    GLOSS_DIV_CLASS: str = "devsite-article-body clearfix"
    REF_URL_FMT: str = MLGlossHTMLScraper.ML_GLOSS_URL + "/#{}"
    ML_GLOSS_ID_FMT: str = "ml_gloss|{}"
    # reg expressions
    # note: .* does not match new line.
    TOPIC_SENT_REGEXP = re.compile(r"^[\s\S]*?[.|:]")
    IMG_SRC_REGEXP = re.compile(r"/machine-learning/glossary/images/")
    CATEGORY_REGEXP = re.compile(r"<div class=\"glossary-icon\" title=\"(.*)\">.*</div>")
    # regular expression objects to be used for parsing
    CONTENTS_DELIM_REGEXP = re.compile("<p><a class=\"glossary-anchor\" name=\".*\"></a>\n</p>"
                                       "<h2 class=\"hide-from-toc\" data-text=\".*\" id=\".*\" "
                                       "tabindex=\"[0-9]\">.*</h2>")
    META_REGEXP = re.compile("<p><a class=\"glossary-anchor\" name=\"(.*)\"></a>\n</p>"
                             "<h2 class=\"hide-from-toc\" data-text=\"(.*)\" id=\".*\" tabindex=\"[0-9]\">.*</h2>")
    GLOSS_H2_REGEXP = re.compile("<h2 class=\"glossary\" data-text=\".*\" id=\".*\" tabindex=\"[0-9]\">.*</h2>")
    GLOSS_ANC_REGEXP = re.compile("<a class=\"glossary-anchor\" name=\".*\"></a>")
    CATEGORY_DIV_1_REGEXP = re.compile("<div class=\"glossary-icon-container\">\n"
                                       "<div class=\"glossary-icon\" title=\".*\">.*</div>\n"
                                       "</div>")
    CATEGORY_DIV_2_REGEXP = re.compile("<div class=\"glossary-icon-container\">\n"
                                       "<div class=\"glossary-icon\" title=\".*\">.*</div>\n"
                                       "<div class=\"glossary-icon\" title=\".*\">.*</div>\n"
                                       "</div>")
    EMPTY_P_REGEXP = re.compile("<p></p>")
    # to be used for filer out the description part
    DESC_RAW_FILTER_REGEXP = re.compile("|".join([
        regexp.pattern for regexp in [GLOSS_H2_REGEXP,
                                      GLOSS_ANC_REGEXP,
                                      CATEGORY_DIV_1_REGEXP,
                                      CATEGORY_DIV_2_REGEXP,
                                      EMPTY_P_REGEXP]
    ]))

    @classmethod
    def parse(cls, src_html: str) -> Generator[MLGloss, None, None]:
        gloss_div = cls._ext_gloss_div(src_html)
        ml_gloss_ids = cls._ext_ml_gloss_ids(gloss_div)
        words = cls._ext_words(gloss_div)
        refs = cls._ext_refs(gloss_div)
        categories = cls._ext_categories(gloss_div)
        descs = cls._ext_ml_gloss_descs(gloss_div)
        # so clean! I love comprehensions syntax + zip
        return (
            MLGloss().set_all(ml_gloss_id, word, ref, category, desc)
            for ml_gloss_id, word, ref, category, desc
            in zip(ml_gloss_ids, words, refs, categories, descs)
        )

    @classmethod
    def _ext_ml_gloss_descs(cls, gloss_div: BeautifulSoup) -> Generator[MLGlossDesc, None, None]:
        desc_raws = cls._ext_desc_raws(gloss_div)
        pure_texts = cls._ext_pure_texts(gloss_div)
        topic_sents = cls._ext_topic_sents(gloss_div)
        return (
            MLGlossDesc().set_all(desc_raw, pure_text, topic_sent)
            for desc_raw, pure_text, topic_sent
            in zip(desc_raws, pure_texts, topic_sents)
        )

    @classmethod
    def _ext_gloss_div(cls, src_html: str) -> BeautifulSoup:
        soup = BeautifulSoup(src_html, 'html.parser')
        gloss_div = soup.find("div", attrs={'class': cls.GLOSS_DIV_CLASS})
        return gloss_div

    @classmethod
    def _ext_ml_gloss_ids(cls, gloss_div: BeautifulSoup) -> Generator[str, None, None]:
        metas = cls._ext_metas(gloss_div)
        return (
            cls.ML_GLOSS_ID_FMT.format(meta[0].strip())
            for meta in metas
        )

    @classmethod
    def _ext_words(cls, gloss_div: BeautifulSoup) -> Generator[str, None, None]:
        metas = cls._ext_metas(gloss_div)
        return (
            meta[1].strip()
            for meta in metas
        )

    @classmethod
    def _ext_refs(cls, gloss_div: BeautifulSoup) -> Generator[str, None, None]:
        return (
            cls.REF_URL_FMT.format(ml_gloss_id)
            for ml_gloss_id in cls._ext_ml_gloss_ids(gloss_div)
        )

    @classmethod
    def _ext_categories(cls, gloss_div: BeautifulSoup) -> Generator[str, None, None]:
        """
        category raw may not exist.
        e.g. <div class="glossary-icon" title="Sequence Models">#seq</div>
        """
        contents = cls._ext_contents(gloss_div)
        soups = (
            BeautifulSoup(content, 'html.parser')
            for content in contents
        )  # soup generator
        category_raws = (
            soup.find('div', attrs={'class': 'glossary-icon'})
            for soup in soups
        )  # category_raws generator
        categories = (
            cls.CATEGORY_REGEXP.findall(category_raw)[0]
            if category_raw else None
            for category_raw in category_raws
        )
        return categories

    @classmethod
    def _ext_desc_raws(cls, gloss_div: BeautifulSoup) -> Generator[str, None, None]:
        contents = cls._ext_contents(gloss_div)
        soups = (
            BeautifulSoup(content, 'html.parser')
            for content in contents
        )  # soup generator
        desc_raws = (
            cls.DESC_RAW_FILTER_REGEXP.sub(repl="", string=str(soup).strip())
            for soup in soups
        )  # desc_raws generator
        # insert the image urls and return
        return (
            cls.IMG_SRC_REGEXP.sub(repl=cls.IMAGES_URL, string=desc_raw)
            for desc_raw in desc_raws
        )

    @classmethod
    def _ext_pure_texts(cls, gloss_div: BeautifulSoup) -> Generator[str, None, None]:
        return (
            BeautifulSoup(desc_raw, 'html.parser').get_text().strip()
            for desc_raw in cls._ext_desc_raws(gloss_div)
        )

    @classmethod
    def _ext_topic_sents(cls, gloss_div: BeautifulSoup) -> Generator[str, None, None]:
        return (
            cls.TOPIC_SENT_REGEXP.findall(string=pure_text)[0]
            for pure_text in cls._ext_pure_texts(gloss_div)
        )

    @classmethod
    def _ext_contents(cls, gloss_div: BeautifulSoup) -> List[str]:
        return cls.CONTENTS_DELIM_REGEXP.split(str(gloss_div))

    @classmethod
    def _ext_metas(cls, gloss_div: BeautifulSoup) -> List[str]:
        return cls.META_REGEXP.findall(str(gloss_div))
