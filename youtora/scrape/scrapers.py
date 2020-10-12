# for type hinting
from typing import List, Generator
# for checking when to stop loading uploads
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.common.by import By
from .models import TracksRaw, ChannelRaw, VideoRaw
from .dataclasses import CaptionData, CaptionsRawData
import youtube_dl
import requests
import logging
from selenium import webdriver


class Scraper:
    # chrome drivers are stored in bin
    CHROME_DRIVER_PATH: dict = {
        "mac": "./bin/chromedriver_mac64",
        "linux": "./bin/chromedriver_linux64"
    }
    # I'm using this for now..
    MOBILE_OPT: dict = {"deviceName": "Nexus 5"}

    @classmethod
    def scrape(cls, **kwargs):
        """
        scrape a single object.
        """
        raise NotImplementedError

    @classmethod
    def scrape_page_src(cls, driver: webdriver.Chrome, url: str) -> str:
        """
        scrape the page source using selenium driver.
        use this in the case where scraping with requests does not work.
        """
        driver.get(url)
        src_html = driver.page_source
        return src_html

    @classmethod
    def get_driver(cls,
                   is_silent: bool = False,
                   is_mobile: bool = False,
                   os: str = "mac",
                   time_out: int = 10) -> webdriver.Chrome:
        """
        get a chrome driver
        :param os:
        :param time_out:
        :param is_mobile:
        :param is_silent:
        :return:
        """
        # get the path to the chrome driver
        chrome_driver_path = cls.CHROME_DRIVER_PATH.get(os, None)
        if not chrome_driver_path:
            raise ValueError("invalid os name: " + os)

        # using mobile environment
        chrome_options = webdriver.ChromeOptions()
        #  open a mobile one
        #  opening with a mobile option will reduce the
        #  time it takes to load the page
        if is_mobile:
            chrome_options.add_experimental_option("mobileEmulation", cls.MOBILE_OPT)
        # do it silently (the gui won't open)
        if is_silent:
            chrome_options.add_argument('headless')
        # get the driver instance with the options
        driver = webdriver.Chrome(executable_path=chrome_driver_path,
                                  options=chrome_options)
        # implicitly wait. Wait until the timeout given passes.
        driver.implicitly_wait(time_out)
        # the driver to use
        return driver


class TracksRawScraper(Scraper):
    @classmethod
    def scrape(cls, caption: CaptionData) -> TracksRaw:
        """
        :param caption: parsed caption object.
        :return:
        """
        logger = logging.getLogger("scrape")
        logger.info("loading tracks...:" + caption.url)
        response = requests.get(caption.url)  # first, get the response (download)
        response.raise_for_status()  # check if the response was erroneous
        tracks_raw = TracksRaw(_id="|".join([caption.id, "tracks"]),
                               caption_id=caption.id,
                               raw_xml=response.text)
        # should be saved later. scrape does scraping only.
        return tracks_raw

    @classmethod
    def scrape_multi(cls, caption_list: List[CaptionData]) -> Generator[TracksRaw, None, None]:
        # returns a generator
        return (
            cls.scrape(caption)
            for caption in caption_list
        )


class CaptionsRawDataScraper:
    @classmethod
    def scrape(cls, video_raw: VideoRaw) -> CaptionsRawData:
        """
        :param video_raw:
        :return:
        """
        video_info = video_raw.video_info
        manual_captions_info: dict = video_info.pop('subtitles')
        auto_captions_info: dict = video_info.pop('automatic_captions')
        # assign and return
        captions_raw = CaptionsRawData(video_id=video_raw.id,
                                       manual_captions_info=manual_captions_info,
                                       auto_captions_info=auto_captions_info)
        return captions_raw

    @classmethod
    def scrape_multi(cls, video_raw_list: List[VideoRaw]) -> Generator[CaptionsRawData, None, None]:
        """
        :param video_raw_list: list of VideoRaw objects.
        :return:
        """
        return (
            cls.scrape(video_raw)
            for video_raw in video_raw_list
        )


class VideoRawScraper:
    VIDEO_DL_OPTS = {
        'writesubtitles': True,
        'allsubtitles': True,
        'writeautomaticsub': True,
        'writeinfojson': True,
        'quiet': True
    }  # VIDEO_DL_OPTIONS

    @classmethod
    def scrape(cls, vid_id: str, channel_raw: ChannelRaw) -> VideoRaw:
        """
        given youtube video url, returns the meta data of the channel_raw
        """
        # get the info.
        with youtube_dl.YoutubeDL(cls.VIDEO_DL_OPTS) as ydl:
            video_info: dict = ydl.extract_info(url=vid_id, download=False)
        # assign and return. make sure to save them later.
        video_raw = VideoRaw(_id=vid_id, channel_raw=channel_raw,
                             video_info=video_info)
        return video_raw

    @classmethod
    def scrape_multi(cls, vid_id_list: List[str], channel_raw: ChannelRaw) -> Generator[VideoRaw, None, None]:
        """
        returns a generator.
        :param vid_id_list:
        :param channel_raw:
        :return: a generator of video_raw objects
        """
        logger = logging.getLogger("scrape_multi")
        for vid_id in vid_id_list:
            try:
                # try scraping video for this
                video_raw = cls.scrape(vid_id, channel_raw)
            except youtube_dl.utils.DownloadError as de:
                # if downloading the video fails, log and just skip this one
                logger.warning(de)
                continue
            else:
                # yield the video
                yield video_raw


class ChannelRawScraper(Scraper):
    # the url to the playlist for getting all uploaded videos
    CHAN_UPLOADS_URL = "https://m.youtube.com/channel/{}/videos?view=0&flow=list"
    # the main landing page of the channel_raw
    CHAN_URL = "http://www.youtube.com/channel/{}"
    # the show more button changes its position. find it by its class name
    SHOW_MORE_CLASS = "nextcontinuation-button"
    TIME_OUT = 5

    @classmethod
    def scrape(cls,
               channel_id: str,
               lang_code: str,
               os: str,
               is_silent: bool = True,
               is_mobile: bool = True) -> ChannelRaw:
        """
        :return: an unparsed channel_raw object
        """
        logger = logging.getLogger("scrape")
        driver = super().get_driver(is_silent, is_mobile, os)
        # get the driver
        try:
            # scrape the two html's
            chan_url = cls.CHAN_URL.format(channel_id)
            main_html = cls._scrape_main(driver, chan_url)
            uploads_url = cls.CHAN_UPLOADS_URL.format(channel_id)
            uploads_html = cls._scrape_uploads(driver, uploads_url)
        except Exception as e:
            raise e
        else:
            # assign and return
            channel_raw = ChannelRaw(_id=channel_id, url=chan_url,
                                     lang_code=lang_code, main_html=main_html,
                                     uploads_html=uploads_html)
            return channel_raw
        finally:
            logger.info("quitting the driver...")
            driver.quit()

    @classmethod
    def _scrape_main(cls, driver: webdriver.Chrome, chan_url: str) -> str:
        logger = logging.getLogger("_scrape_main")
        logger.info("loading main page...: " + chan_url)
        main_html = super().scrape_page_src(driver, chan_url)
        return main_html

    @classmethod
    def _scrape_uploads(cls, driver: webdriver.Chrome, uploads_url: str) -> str:
        logger = logging.getLogger("_scrape_uploads")
        logger.info("loading uploads page...: " + uploads_url)
        driver.get(uploads_url)
        # now we have to load all the videos, by repeatedly clicking the "show more" button.
        load_cnt = 0
        while True:
            try:
                # try getting the show more button
                show_more_button = WebDriverWait(driver, cls.TIME_OUT).until(
                    e_c.element_to_be_clickable((By.CLASS_NAME, cls.SHOW_MORE_CLASS))
                )
            except TimeoutException as nse:
                logger.debug(str(nse))
                # on timeout, break the loop
                break
            else:
                # scroll down
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                # click the button
                show_more_button.click()
                # while load more button is clickable..
                load_cnt += 1
                logger.info("loading uploads #" + str(load_cnt))
        # return the source
        uploads_html = driver.page_source
        return uploads_html


class MLGlossHTMLScraper(Scraper):
    # get all the definitions from here
    ML_GLOSS_URL = "https://developers.google.com/machine-learning/glossary"

    @classmethod
    def scrape(cls) -> str:
        logger = logging.getLogger("scrape")
        driver = super().get_driver(is_silent=True,
                                    is_mobile=True)
        try:
            logger.info("loading ml glossary page...: " + cls.ML_GLOSS_URL)
            super(MLGlossHTMLScraper, cls).scrape_page_src(driver, cls.ML_GLOSS_URL)
        except Exception as e:
            raise e
        else:
            mlgloss_html = driver.page_source
            return mlgloss_html
        finally:
            logger.info("quitting the driver...")
            driver.quit()