from typing import Tuple

from selenium import webdriver
import re
import logging
import sys
# https://stackoverflow.com/questions/20333674/pycharm-logging-output-colours/45534743
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class Scraper:
    # for now, put the executable in the same directory
    CHROME_DRIVER_PATH = "./src/youtube/scrape/chromedriver"

    # I'm using this for now..
    MOBILE_OPT = {"deviceName": "Nexus 5"}

    @classmethod
    def get_driver(cls,
                   time_out: int = 5,
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

        # implicitly wait. Wait for 10 seconds.
        driver.implicitly_wait(time_out)

        # the driver to use
        return driver


class ChannelScraper(Scraper):
    """
    keep in mind that the subs count is only
    a rough value.
    """
    @classmethod
    def subs(cls, chan_url) -> int:
        logger = logging.getLogger("subs")

        # get the driver
        driver = super().get_driver(is_mobile=True,
                                    is_silent=True)
        # try getting the driver
        # look for the subs, get the xpath
        logger.info("loading page...")
        driver.get(chan_url)

        subs_elem = driver.find_element_by_xpath(
            "//*[@id=\"app\"]/div[1]/ytm-browse/ytm-c4-tabbed-header-renderer/div/div/div/span"
        )

        # get the data
        subs_data = subs_elem.text.split(" ")[0].strip()

        # Now I have to parse this
        if re.match(r'[\d,]*[KMB]$', subs_data):
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


class VideoScraper(Scraper):
    """
    just focus on this for now
    likes, dislikes.
    :return a tuple (likes, dislikes)
    """
    @classmethod
    def likes_dislikes(cls, vid_url) -> Tuple[int, int]:
        """
        get the meta data for video,
        except for captions
        """
        logger = logging.getLogger("get_likes_dislikes")

        # get it with a mobile version
        driver = super().get_driver(is_mobile=True,
                                    is_silent=True)

        # get the url - this might take a while
        logger.info("downloading video page...")
        driver.get(vid_url)

        # get the elements by xpath
        like_elem = driver.find_element_by_xpath(
            "//*[@id=\"app\"]/" +
            "div[2]/ytm-watch/" +
            "ytm-single-column-watch-next-results-renderer/" +
            "ytm-item-section-renderer[1]/" +
            "lazy-list/" +
            "ytm-slim-video-metadata-renderer/" +
            "div[2]/" +
            "c3-material-button[1]/button/" +
            "div/div/span"
        )

        dislike_elem = driver.find_element_by_xpath(
            "//*[@id=\"app\"]/" +
            "div[2]/ytm-watch/" +
            "ytm-single-column-watch-next-results-renderer/" +
            "ytm-item-section-renderer[1]/" +
            "lazy-list/ytm-slim-video-metadata-renderer/" +
            "div[2]/c3-material-button[2]/button/div/div/span"
        )

        # now check them out
        like_cnt = int(like_elem
                       .get_attribute("aria-label")
                       .split(" ")[0]
                       .replace(",", ""))

        # dislike count
        dislike_cnt = int(dislike_elem
                          .get_attribute("aria-label")
                          .split(" ")[0]
                          .replace(",", ""))

        return like_cnt, dislike_cnt
