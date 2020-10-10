from typing import List, Tuple, Generator
from selenium import webdriver
from ..common import Scraper
from .models import MLGlossRaw
import logging
import re
from bs4 import BeautifulSoup

x
class MLGlossRawScraper(Scraper):
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
    def scrape(cls) -> List[MLGlossRaw]:
        driver = super().get_driver(is_silent=True,
                                    is_mobile=True)
        return cls.dl_and_parse(driver)

    @classmethod
    def dl_and_parse(cls, driver: webdriver.Chrome) -> List[MLGlossRaw]:
        logger = logging.getLogger("dl_and_parse")
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
    def _parse_html(cls, html: str) -> Tuple[Generator[dict, None, None], Generator[dict, None, None]]:
        soup = BeautifulSoup(html, 'html.parser')
        gloss_div = soup.find("div", attrs={'class': "devsite-article-body clearfix"})
        parsed_contents = cls._parse_contents(gloss_div)
        parsed_metas = cls._parse_metas(gloss_div)
        return parsed_contents, parsed_metas

    @classmethod
    def _parse_contents(cls, gloss_div: BeautifulSoup) -> Generator[dict, None, None]:
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
        parsed_contents = (
            {
                "desc_raw": desc_raw,
                "category_raw": str(category_raw).strip() if category_raw else None
            }
            for desc_raw in desc_raws
            for category_raw in category_raws
        )  # action; build parsed_contents list
        return parsed_contents

    @classmethod
    def _parse_metas(cls, gloss_div: BeautifulSoup) -> Generator[dict, None, None]:
        # get the meta
        metas = cls.META_REGEXP.findall(str(gloss_div))
        parsed_metas = (
            {
                "id": meta[0].strip(),
                "word": meta[1].strip()
            }
            for meta in metas
        )
        return parsed_metas


