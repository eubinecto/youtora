
from selenium import webdriver

from src.youtube.dload.models import Video
import logging
import sys
# https://stackoverflow.com/questions/20333674/pycharm-logging-output-colours/45534743
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class Scraper:
    # for now, put the executable in the same directory
    CHROME_DRIVER_PATH = "./src/youtube/scrape/chromedriver"

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
    not getting the subs yet.
    """
    pass


class VideoScraper(Scraper):
    """
    just focus on this for now
    likes, dislikes.
    :return a tuple (likes, dislikes)
    """
    @classmethod
    def get_likes_dislikes(cls, vid_url):
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
        like_cnt = int(like_elem.get_attribute("aria-label")
                       .split(" ")[0]
                       .replace(",", ""))

        # dislike count
        dislike_cnt = int(dislike_elem.get_attribute("aria-label")
                          .split(" ")[0]
                          .replace(",", ""))

        return like_cnt, dislike_cnt
