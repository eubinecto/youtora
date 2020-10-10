from selenium import webdriver


class Scraper:
    # chrome drivers are stored in bin
    CHROME_DRIVER_PATH: dict = {
        "mac": "./be/bin/chromedriver_mac64",
        "linux": "./be/bin/chromedriver_linux64"
    }
    # I'm using this for now..
    MOBILE_OPT: dict = {"deviceName": "Nexus 5"}

    @classmethod
    def scrape(cls, **kwargs):
        """
        entry point
        """
        raise NotImplementedError

    @classmethod
    def dl_and_parse(cls, **kwargs):
        """
        download and parse into corresponding dataclass. (Video,Track,Caption, etc)
        """
        raise NotImplementedError

    @classmethod
    def get_driver(cls,
                   os: str = "mac",
                   time_out: int = 10,
                   is_mobile: bool = False,
                   is_silent: bool = False) -> webdriver.Chrome:
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