import json
from typing import Tuple, List, Optional

from selenium import webdriver

# for checking when to stop loading uploads
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
from functional import seq

import requests
import re
import logging
import sys
# https://stackoverflow.com/questions/20333674/pycharm-logging-output-colours/45534743
from be.src.mongo.settings import CorporaDB
from be.src.youtora.dataclasses import Channel, MLGlossRaw, MLGloss, MLGlossDesc

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class HTMLParser:
    # chrome drivers are stored in bin
    CHROME_DRIVER_PATH_DICT = {
        "mac": "./be/bin/chromedriver_mac64",
        "linux": "./be/bin/chromedriver_linux64"
    }
    # I'm using this for now..
    MOBILE_OPT = {"deviceName": "Nexus 5"}

    @classmethod
    def get_driver(cls,
                   os: str,
                   time_out: int = 10,
                   is_mobile: bool = False,
                   is_silent: bool = False):
        # get the path to the chrome driver
        chrome_driver_path = cls.CHROME_DRIVER_PATH_DICT.get(os, None)
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


class ChannelHTMLParser(HTMLParser):
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

    CHAN_URL_FORMAT = "http://www.youtube.com/channel/{}"

    @classmethod
    def parse(cls,
              chan_url: str,
              lang_code: str,
              os: str) -> Channel:
        """
        now you might be able to do this.
        :param os:
        :param chan_url: the id of the channel
        :param lang_code
        :return: a channel object
        """
        logger = logging.getLogger("scrape_channel")
        # get the driver
        driver = super().get_driver(is_silent=True,
                                    is_mobile=True,
                                    os=os)

        # get the channel page to get the channel id, subs, uploader
        try:
            logger.info("loading channel page...")
            driver.get(chan_url)
            channel_id = cls._channel_id(driver)
            uploader = cls._uploader(driver)
            subs = cls._subs(driver)
            # get the uploads page
            logger.info("loading uploads page...")
            driver.get(cls.CHAN_ALL_UPLOADS_URL.format(chan_id=channel_id))
            vid_id_list = cls._vid_id_list(driver)
        except Exception as e:
            raise e
        else:
            # the channel is given a lang code
            return Channel(id=channel_id,
                           url=cls.CHAN_URL_FORMAT.format(channel_id),
                           title=uploader,
                           subs=subs,
                           lang_code=lang_code,
                           vid_id_list=vid_id_list)
        finally:
            logger.info("quitting the driver")
            driver.quit()

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
                subs_cnt = int(float(subs_data[:-1]) * (10 ** 3))
            elif subs_data[-1] == 'M':
                subs_cnt = int(float(subs_data[:-1]) * (10 ** 6))
            else:
                # has a billion subs
                subs_cnt = int(float(subs_data[:-1]) * (10 ** 9))
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


class VideoHTMLParser(HTMLParser):
    """
    just focus on this for now
    likes, dislikes.
    """

    @classmethod
    def likes_dislikes(cls,
                       vid_url) -> Tuple[int, int]:
        """
        get the meta data for video,
        except for captions
        """
        headers = {
            # get the english page
            "Accept-Language": "en"
        }
        # get the page
        html = requests.get(url=vid_url, headers=headers).text
        # the first will be like info, the latter will be dislike info
        results = re.findall(r'"toggleButtonRenderer":{.*?"accessibilityData":{"label":"(.*?)"}}', html)
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


class MLGlossRawHTMLParser(HTMLParser):
    # get all the definitions from here
    ML_GLOSS_ENDPOINT = "https://developers.google.com/machine-learning/glossary"
    CREDIT_FORMAT = ML_GLOSS_ENDPOINT + "/#{}"
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
    def parse(cls) -> List[MLGlossRaw]:
        logger = logging.getLogger("scrape_ml_gloss_raw")
        driver = super().get_driver(is_silent=True,
                                    is_mobile=True)
        try:
            # get the html
            logger.info("loading ml glossary page...")
            driver.get(cls.ML_GLOSS_ENDPOINT)
            html = driver.page_source
        except Exception as e:
            raise e
        else:
            # parse html to get the result you want
            parsed_contents, parsed_metas = cls._parse_html(html)
            ml_gloss_raws = [
                MLGlossRaw(id="ml_gloss_raw|" + parsed_meta['id'],
                           word=parsed_meta['word'],
                           credit=cls.CREDIT_FORMAT.format(parsed_meta['id']),
                           desc_raw=parsed_content['desc_raw'],
                           category_raw=parsed_content['category_raw'])
                for parsed_content, parsed_meta in zip(parsed_contents, parsed_metas)
            ]
            return ml_gloss_raws
        finally:
            logger.info("quitting the driver")
            driver.quit()

    @classmethod
    def _parse_html(cls, html: str) -> Tuple[List[dict], List[dict]]:
        soup = BeautifulSoup(html, 'html.parser')
        gloss_div = soup.find("div", attrs={'class': "devsite-article-body clearfix"})
        parsed_contents = cls._parse_contents(gloss_div)
        parsed_metas = cls._parse_metas(gloss_div)
        return parsed_contents, parsed_metas

    @classmethod
    def _parse_contents(cls, gloss_div: BeautifulSoup) -> List[dict]:
        # split them by this delimiter
        contents = cls.CONTENTS_DELIM_REGEXP.split(str(gloss_div))
        soups = (
            BeautifulSoup(content, 'html.parser')
            for content in contents
        )  # soup generator
        desc_raws = (
            cls.DESC_RAW_FILTER_REGEXP.sub(repl="", string=str(soup).strip())
            for soup in soups
        )  # desc_raws generator
        category_raws = (
            soup.find('div', attrs={'class': 'glossary-icon'})
            for soup in soups
        )  # category_raws generator
        parsed_contents = [
            {
                "desc_raw": desc_raw,
                "category_raw": str(category_raw).strip() if category_raw else None
            }
            for desc_raw in desc_raws
            for category_raw in category_raws
        ]  # action; build parsed_contents list
        return parsed_contents

    @classmethod
    def _parse_metas(cls, gloss_div: BeautifulSoup) -> List[dict]:
        # get the meta
        metas = cls.META_REGEXP.findall(str(gloss_div))
        parsed_metas = [
            {
                "id": meta[0].strip(),
                "word": meta[1].strip()
            }
            for meta in metas
        ]
        return parsed_metas


class DataParser:
    """
    the class for parsing a Data model.
    """
    pass


class MLGlossRawParser(DataParser):
    """
    houses logic for parsing raw MLGloss
    """
    # format with the file name of the svg file
    IMAGES_ENDPOINT = "https://developers.google.com/machine-learning/glossary/images/"
    # note: .* does not match new line.
    TOPIC_SENT_REGEXP = re.compile(r"^[\s\S]*?[.|:]")
    IMG_SRC_REGEXP = re.compile(r"/machine-learning/glossary/images/")
    CATEGORY_REGEXP = re.compile(r"<div class=\"glossary-icon\" title=\"(.*)\">.*</div>")

    @classmethod
    def parse(cls) -> List[MLGloss]:
        corpora_db = CorporaDB()
        # get MlGlossRaw data
        ml_gloss_raws: List[MLGlossRaw] = [
            MLGlossRaw(id=res['_id'],
                       word=res['word'],
                       credit=res['credit'],
                       desc_raw=res['desc_raw'],
                       category_raw=res['category_raw'])
            for res in list(corpora_db.ml_gloss_raw_coll.find())
        ]
        # parse it into ml glosses
        ml_glosses: List[MLGloss] = [
            MLGloss(id="ml_gloss|" + ml_gloss_raw.id.split("|")[-1],
                    word=ml_gloss_raw.word,
                    credit=ml_gloss_raw.credit,
                    desc=cls._parse_desc_raw(ml_gloss_raw.desc_raw),
                    category=cls._parse_category_raw(ml_gloss_raw.category_raw))
            for ml_gloss_raw in ml_gloss_raws
        ]
        # return it
        return ml_glosses

    @classmethod
    def _parse_desc_raw(cls, desc_raw: str) -> MLGlossDesc:
        desc_raw = cls.IMG_SRC_REGEXP.sub(repl=cls.IMAGES_ENDPOINT, string=desc_raw)
        desc_raw_bs = BeautifulSoup(desc_raw, 'html.parser')
        pure_text = desc_raw_bs.get_text().strip()
        topic_sent = cls.TOPIC_SENT_REGEXP.findall(string=pure_text)[0]
        return MLGlossDesc(topic_sent=topic_sent,
                           pure_text=pure_text,
                           desc_raw=desc_raw)

    @classmethod
    def _parse_category_raw(cls, category_raw: Optional[str]) -> Optional[str]:
        """
        category raw may not exist.
        e.g. <div class="glossary-icon" title="Sequence Models">#seq</div>
        """
        if category_raw:
            return cls.CATEGORY_REGEXP.findall(category_raw)[0]
        return None
