from typing import List, Generator, Tuple

# for checking when to stop loading uploads
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.common.by import By

from ..common import Scraper
from .builders import CaptionBuilder
from .dataclasses import Video, Track, Caption, Channel
# use youtube_dl for getting the automatic captions
import youtube_dl
import requests
import html
import xmltodict
import logging
from selenium import webdriver
import re


class TrackScraper(Scraper):

    @classmethod
    def scrape(cls, caption: Caption) -> List[Track]:
        """
        main function
        :return:
        """
        tracks = cls.dl_and_parse(caption)
        # set the prev_id & next_id in this tracks batch
        cls._set_neighbours(tracks=tracks)
        # set the context
        cls._set_contexts(tracks=tracks)
        return tracks

    @classmethod
    def dl_and_parse(cls, caption: Caption) -> List[Track]:
        logger = logging.getLogger("dl_and_parse")
        tracks = list()  # bucket to collect tracks
        response = requests.get(caption.url)  # first, get the response (download)
        response.raise_for_status()  # check if the response was erroneous
        tracks_xml = html.unescape(response.text)  # get the xml. escape the character reference entities
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
                    track = Track(parent_id=caption.id,
                                  start=start,
                                  duration=duration,
                                  content=content)
                    tracks.append(track)
        return tracks

    @classmethod
    def _set_neighbours(cls, tracks: List[Track]):
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
    def _set_contexts(cls, tracks: List[Track]):
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


class VideoScraper:
    VIDEO_DL_OPTS = {
        'writesubtitles': True,
        'allsubtitles': True,
        'writeautomaticsub': True,
        'writeinfojson': True,
        'quiet': True
    }  # VIDEO_DL_OPTIONS

    VID_URL_FORMAT = "https://www.youtube.com/watch?v={}"

    HEADERS = {
        # get the english page
        "Accept-Language": "en"
    }

    @classmethod
    def scrape(cls,
               vid_id_list: List[str],
               batch_info: str = None) -> Generator[Video, None, None]:
        """
        returns a generator that yields videos.
        :param vid_id_list:
        :param batch_info:
        :return:
        """
        total_vid_cnt = len(vid_id_list)
        vid_done = 0
        # https://stackoverflow.com/questions/11548674/logging-info-doesnt-show-up-on-console-but-warn-and-error-do/11548754
        vid_logger = logging.getLogger("dl_videos_lazy")
        if not vid_id_list:
            # if there are no ids, then yield None
            yield None
        else:
            for vid_id in vid_id_list:
                # make a vid_url
                vid_url = "https://www.youtube.com/watch?v={}".format(vid_id)
                try:
                    # try scraping the video
                    video = cls.dl_and_parse(vid_url=vid_url)
                except youtube_dl.utils.DownloadError as de:
                    # if downloading the video fails, log and just skip this one
                    vid_logger.warning(de)
                    continue
                else:
                    # report
                    vid_done += 1
                    vid_logger.info("dl vid objects done: {}/{}/batch={}".format(vid_done,
                                                                                 total_vid_cnt,
                                                                                 batch_info))
                    # yield the video
                    yield video

    @classmethod
    def dl_and_parse(cls, vid_url: str) -> Video:
        """
        given youtube video url, returns the meta data of the channel
        :param vid_url: the url of the video
        :return: a Video object
        """
        # get the info.
        with youtube_dl.YoutubeDL(cls.VIDEO_DL_OPTS) as ydl:
            info = ydl.extract_info(url=vid_url, download=False)

        # access the results
        vid_id = info['id']
        title = info['title']
        channel_id = info['channel_id']
        upload_date = "{year}-{month}-{day}" \
            .format(year=info['upload_date'][:4],
                    month=info['upload_date'][4:6],
                    day=info['upload_date'][6:])  # e.g. 20200610 -> 2020-06-10
        manual_sub_info = info['subtitles']
        auto_sub_info = info['automatic_captions']
        views = info['view_count']
        # the length is always greater than zero
        # use the first one as the category of this video
        category = info['categories'][0]

        # better collect these info separately
        likes, dislikes = cls._parse_likes_dislikes(vid_url)

        # creates a video object
        video = Video(id=vid_id,
                      title=title,
                      url=cls.VID_URL_FORMAT.format(vid_id),
                      parent_id=channel_id,
                      publish_date=upload_date,
                      likes=likes,
                      dislikes=dislikes,
                      views=views,
                      category=category,
                      manual_sub_info=manual_sub_info,
                      auto_sub_info=auto_sub_info)
        # set captions and tracks
        cls._build_and_set_captions(video)
        cls._dl_and_set_tracks(video)
        return video

    @classmethod
    def _parse_likes_dislikes(cls, vid_url) -> Tuple[int, int]:
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
    def _build_and_set_captions(cls, video: Video):
        captions = CaptionBuilder(video).build_captions()
        video.set_captions(captions)

    @classmethod
    def _dl_and_set_tracks(cls, video: Video):
        logger = logging.getLogger("_dl_and_set_tracks")
        # download the tracks
        done = 0
        total = len(video.captions)
        for idx, caption in enumerate(video.captions):
            # download and set tracks
            tracks = TrackScraper.scrape(caption)
            caption.set_tracks(tracks)
            done += 1
            logger.info("({}/{}), downloading tracks complete for caption:{}"
                        .format(done, total, caption))


class ChannelScraper(Scraper):
    # the url to the playlist for getting all uploaded videos
    # fill in the channel Id
    CHAN_ALL_UPLOADS_URL = "https://m.youtube.com/channel/{chan_id}/videos?view=0&flow=list"
    # XPaths for the elements that we want to access
    # inspect these from chrome browser
    CHAN_LINK_XPATH = "/html/head/link[4]"
    CHAN_TITLE_XPATH = "/html/head/title"
    CHAN_SUB_CNT_CLASS = "c4-tabbed-header-subscriber-count"  # get rid of th empty space
    # the show more button changes its position. find it by its class name
    SHOW_MORE_CLASS = "nextcontinuation-button"
    CHAN_URL_FORMAT = "http://www.youtube.com/channel/{chan_id}"

    @classmethod
    def scrape(cls,
               chan_url: str,
               lang_code: str,
               os: str,
               is_silent: bool = True,
               is_mobile: bool = True) -> Channel:
        """
        :return: a channel object
        """
        # get the driver
        driver = super().get_driver(is_silent=is_silent,
                                    is_mobile=is_mobile,
                                    os=os)
        # get the channel
        channel = cls.dl_and_parse(driver, chan_url, lang_code)
        # return the channel
        return channel

    @classmethod
    def dl_and_parse(cls,
                     driver: webdriver.Chrome,
                     chan_url: str,
                     lang_code: str) -> Channel:
        logger = logging.getLogger("dl_and_parse")
        # get the channel page to get the channel id, subs, title
        try:
            logger.info("loading channel page...")
            driver.get(chan_url)
            channel_id = cls._parse_channel_id(driver)
            title = cls._parse_title(driver)
            subs = cls._parse_subs(driver)
            # get the uploads page
            logger.info("loading uploads page...")
            driver.get(cls.CHAN_ALL_UPLOADS_URL.format(chan_id=channel_id))
            vid_id_list = cls._parse_vid_id_list(driver)
        except Exception as e:
            raise e
        else:
            # the channel is given a lang code
            return Channel(id=channel_id,
                           url=cls.CHAN_URL_FORMAT.format(chan_id=channel_id),
                           title=title,
                           subs=subs,
                           lang_code=lang_code,
                           vid_id_list=vid_id_list)
        finally:
            logger.info("quitting the driver")
            driver.quit()

    @classmethod
    def _parse_channel_id(cls, driver: webdriver.Chrome) -> str:
        chan_link_elem = driver.find_element_by_xpath(cls.CHAN_LINK_XPATH)
        chan_url = chan_link_elem.get_attribute("href").strip()
        # return the last one
        return chan_url.split("/")[-1]

    @classmethod
    def _parse_title(cls, driver: webdriver.Chrome) -> str:
        """
        e.g.
        <title>Abdul Bari - YouTube</title>
        """
        title_elem = driver.find_element_by_xpath(cls.CHAN_TITLE_XPATH)
        return title_elem.text.split("-")[0].strip()

    @classmethod
    def _parse_subs(cls, driver: webdriver.Chrome) -> int:
        """
        keep in mind that the subs count is
        only a rough value.
        e.g.
        <span class="c4-tabbed-header-subscriber-count secondary-text">285K subscribers</span>
        :param driver: the driver that has already loaded the web page
        :return: the approximate sub count of the channel
        """
        span_elem = driver.find_element_by_class_name(cls.CHAN_SUB_CNT_CLASS)
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
    def _parse_vid_id_list(cls, driver: webdriver.Chrome) -> List[str]:
        logger = logging.getLogger("_vid_id_list")
        vid_id_list = list()
        load_cnt = 0
        while True:
            try:
                # try getting the show more button
                show_more_button = WebDriverWait(driver, 5).until(
                    e_c.element_to_be_clickable((By.CLASS_NAME, cls.SHOW_MORE_CLASS))
                )
            except TimeoutException as nse:
                logger.debug(str(nse))
                # how do I know if something went wrong or not..?
                break
            else:
                # scroll down
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                # click the button
                show_more_button.click()
                # while load more button is clickable..
                load_cnt += 1
                logger.info("loading uploads #" + str(load_cnt))
        # get all the elements that are of this class
        videos = driver.find_elements_by_class_name("compact-media-item-image")
        for video in videos:
            link = video.get_attribute('href')
            video_id = link.split("=")[-1].strip()
            vid_id_list.append(video_id)
        # now get the boxes.
        # when everything is done
        # collect the video ids.
        logger.info("video id download complete. # vids total: " + str(len(vid_id_list)))
        return vid_id_list
