from typing import Tuple, List

from selenium import webdriver

# for checking when to stop loading uploads
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.common.by import By

import re
import logging
import sys
# https://stackoverflow.com/questions/20333674/pycharm-logging-output-colours/45534743
from src.youtube.dload.models import Channel
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class Scraper:
    # for now, put the executable in the same directory
    CHROME_DRIVER_PATH = "./src/youtube/scrape/chromedriver"

    # I'm using this for now..
    MOBILE_OPT = {"deviceName": "Nexus 5"}

    @classmethod
    def get_driver(cls,
                   time_out: int = 10,
                   is_mobile: bool = False,
                   is_silent: bool = False):
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
        driver = webdriver.Chrome(executable_path=cls.CHROME_DRIVER_PATH,
                                  options=chrome_options)

        # implicitly wait. Wait until the timeout given passes.
        driver.implicitly_wait(time_out)

        # the driver to use
        return driver


class ChannelScraper(Scraper):
    # the url to the playlist for getting all uploaded videos
    # fill in the channel Id
    CHAN_ALL_UPLOADS_URL = "https://m.youtube.com/channel/{chan_id}/videos?view=0&flow=list"

    # XPaths for the elements that we want to access
    # inspect these from chrome browser
    CHAN_LINK_XPATH = "/html/head/link[4]"
    CHAN_TITLE_XPATH = "//*[@id=\"app\"]/div[1]/ytm-browse/ytm-c4-tabbed-header-renderer/div[2]/div/h1"
    CHAN_SUBS_XPATH = "//*[@id=\"app\"]/div[1]/ytm-browse/ytm-c4-tabbed-header-renderer/div[2]/div/div/span"

    # the show more button changes its position. find it by its class name
    SHOW_MORE_CLASS_NAME = "nextcontinuation-button"

    @classmethod
    def scrape_channel(cls,
                       chan_url: str,
                       driver: webdriver.Chrome = None) -> Channel:
        """
        now you might be able to do this.
        channel_id
        uploader
        subs
        vid_id_list
        :param chan_url: the id of the channel
        :param driver:
        :return: a channel object
        """
        logger = logging.getLogger("scrape_channel")

        if not driver:
            driver_given = False
            # if the driver is not given.. then get the driver yourself.
            driver = super().get_driver(is_silent=True,
                                        is_mobile=True)
        else:
            driver_given = True

        # get the channel page to get the channel id, subs, uploader
        logger.info("loading channel page...")
        driver.get(chan_url)
        channel_id = cls._channel_id(driver)
        uploader = cls._uploader(driver)
        subs = cls._subs(driver)

        # get the uploads page
        logger.info("loading uploads page...")
        driver.get(cls.CHAN_ALL_UPLOADS_URL.format(chan_id=channel_id))

        vid_id_list = cls._vid_id_list(driver)

        if not driver_given:
            # if driver has been made within this method,
            # then close the driver
            driver.close()

        return Channel(channel_id, uploader, subs, vid_id_list)

    @classmethod
    def _channel_id(cls, driver: webdriver.Chrome) -> str:
        chan_link_elem = driver.find_element_by_xpath(cls.CHAN_LINK_XPATH)

        chan_url = chan_link_elem.get_attribute("href").strip()

        # return the last one
        return chan_url.split("/")[-1]

    @classmethod
    def _uploader(cls, driver: webdriver.Chrome) -> str:
        chan_title_elem = driver.find_element_by_xpath(cls.CHAN_TITLE_XPATH)
        return chan_title_elem.text.strip()

    @classmethod
    def _subs(cls, driver: webdriver.Chrome) -> int:
        """
        keep in mind that the subs count is
        only a rough value.
        :param driver: the driver that has already loaded the web page
        :return: the approximate sub count of the channel
        """
        subs_span = driver.find_element_by_xpath(
            cls.CHAN_SUBS_XPATH
        )  # the span element that contains the sub data

        # get the data
        subs_data = subs_span.text.split(" ")[0].strip()

        # Now I have to parse this
        if re.match(r'[\d.]*[KMB]$', subs_data):
            if subs_data[-1] == 'K':
                subs_cnt = int(float(subs_data[:-1]) * (10**3))
            elif subs_data[-1] == 'M':
                subs_cnt = int(float(subs_data[:-1]) * (10**6))
            else:
                # has a billion subs
                subs_cnt = int(float(subs_data[:-1]) * (10**9))
        else:
            # less than 1K
            subs_cnt = int(subs_data)

        # check the value for debugging
        return subs_cnt

    @classmethod
    def _vid_id_list(cls, driver: webdriver.Chrome) -> List[str]:
        logger = logging.getLogger("_vid_id_list")
        vid_id_list = list()
        load_cnt = 0
        while True:
            try:
                # try getting the show more button
                show_more_button = WebDriverWait(driver, 5).until(
                    e_c.element_to_be_clickable((By.CLASS_NAME, cls.SHOW_MORE_CLASS_NAME))
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


class VideoScraper(Scraper):
    """
    just focus on this for now
    likes, dislikes.
    """
    LIKES_XPATH = "//*[@id=\"app\"]/div[2]/ytm-watch/ytm-single-column-watch-next-results-renderer/" \
                   + "ytm-item-section-renderer[1]/lazy-list/ytm-slim-video-metadata-renderer/div[2]/" \
                   + "c3-material-button[1]/button/div/div/span"
    DISLIKES_XPATH = "//*[@id=\"app\"]/div[2]/ytm-watch/ytm-single-column-watch-next-results-renderer/" \
                      + "ytm-item-section-renderer[1]/lazy-list/ytm-slim-video-metadata-renderer/div[2]/" \
                      + "c3-material-button[2]/button/div/div/span"

    @classmethod
    def likes_dislikes(cls,
                       vid_url,
                       driver: webdriver.Chrome = None) -> Tuple[int, int]:
        """
        get the meta data for video,
        except for captions
        """
        logger = logging.getLogger("get_likes_dislikes")

        if not driver:
            driver_given = False
            driver = super().get_driver(is_silent=True,
                                        is_mobile=True)
        else:
            driver_given = True

        # get the url - this might take a while
        logger.info("downloading video page...")
        driver.get(vid_url)

        # get the elements by xpath
        try:
            like_info = driver.find_element_by_xpath(cls.LIKES_XPATH)\
                              .get_attribute("aria-label")\
                              .split(" ")[0]

            dislike_info = driver.find_element_by_xpath(cls.DISLIKES_XPATH) \
                                 .get_attribute("aria-label") \
                                 .split(" ")[0]
        except NoSuchElementException as nse:
            # likes & dislikes are not displayed
            # e.g. https://www.youtube.com/watch?v=tU5D51kExcY
            logger.warning(str(nse))
            # when used as a rank feature..
            # it doesn't have a null_value field
            like_cnt = 0
            dislike_cnt = 0
        else:
            # if the count is zero, then the convention that youtube uses
            # is to replace the value with "No"
            if like_info == "No":
                like_cnt = 0
            else:
                like_cnt = int(like_info.replace(",", ""))

            if dislike_info == "No":
                dislike_cnt = 0
            else:
                dislike_cnt = int(dislike_info.replace(",", ""))

        if not driver_given:
            # if driver has been made within this method,
            # then close the driver
            driver.close()

        return like_cnt, dislike_cnt
