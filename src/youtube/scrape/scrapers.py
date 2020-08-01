
from selenium import webdriver


class Scraper:

    # for now, put the executable in the same directory
    CHROME_DRIVER_PATH = "./src/youtube/scrape/chromedriver"

    MOBILE_OPT = {"deviceName": "Nexus 5"}

    @classmethod
    def get_driver(cls,
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
        driver.implicitly_wait()

        driver.get(url="https://www.youtube.com/watch?v=SXbi6axwOFY")


class ChannelScraper(Scraper):
    """
    video ids
    subs
    """
    pass


class VideoScraper(Scraper):
    """
    likes
    dislikes
    """
    pass
