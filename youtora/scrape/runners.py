# the runners. to be accessed by django console.
from .parsers import CaptionsRawParser, ChannelRawParser
from .scrapers import (
    ChannelRawScraper,
    VideoRawScraper,
    TracksRawScraper,
    CaptionsRawDataScraper
)
import logging
import sys
# logs to standard out, logging level is at info
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class Runner:
    @classmethod
    def run(cls, **kwargs):
        raise NotImplementedError


class ScrapeYouTubeRawsRunner(Runner):
    # just take out the lang codes
    LANG_CODES = [
        lang_code for lang_code, desc
        in CaptionsRawParser.LANG_CODES_TO_COLLECT
    ]

    @classmethod
    def run(cls, channel_id: str, lang_code: str, os: str = "mac"):
        """
        scrapes and saves raw data in the following order:
        1. TracksRaw
        2. VideoRaw (which includes CaptionsRaw)
        3. ChannelRaw
        channel_raw raw is saved at the end.
        """
        assert lang_code in cls.LANG_CODES
        logger = logging.getLogger("run")
        # scrape and store channel_raw raw
        channel_raw = ChannelRawScraper.scrape(channel_id, lang_code, os)
        # scrape and store video raws (which will save caption raws)
        vid_id_list = ChannelRawParser.parse(channel_raw).vid_id_list
        total_vid_cnt = len(vid_id_list)
        video_raws = VideoRawScraper.scrape_multi(vid_id_list, channel_raw)
        for vid_idx, video_raw in enumerate(video_raws):
            # save video_raw
            video_raw.save()
            logger.info("=== {}/{}:video_raw saved:{} ===" .format(vid_idx + 1, total_vid_cnt, str(video_raw)))
            # scrape and store tracks raws
            captions_raw = CaptionsRawDataScraper.scrape(video_raw)
            captions = CaptionsRawParser.parse(captions_raw)
            tracks_raws = TracksRawScraper.scrape_multi(captions)
            for track_idx, tracks_raw in enumerate(tracks_raws):
                tracks_raw.save()
                logger.info("tracks saved #{}".format(track_idx + 1))
        # channel is saved at the end
        channel_raw.save()
        logger.info("channel_raw saved:{}".format(str(channel_raw)))


class ScrapeMLGlossRunner(Runner):
    @classmethod
    def run(cls):
        pass


class ScrapeIdiomsRunner(Runner):
    @classmethod
    def run(cls):
        pass
