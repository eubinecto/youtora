# the runners. to be accessed by django console.
import logging
import sys

from youtora.refine.extractors import CaptionExtractor, ChannelExtractor
from .scrapers import (
    ChannelRawScraper,
    VideoRawScraper,
    TracksRawScraper,
    IdiomRawScraper
)

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
        in CaptionExtractor.LANG_CODES_TO_COLLECT
    ]

    @classmethod
    def run(cls, channel_id: str, lang_code: str, os: str = "mac"):
        """
        scrapes and saves raw data in the following order:
        1. TracksRaw
        2. VideoRaw (which includes CaptionsRaw)
        3. ChannelRaw
        channel_id raw is saved at the end.
        """
        assert lang_code in cls.LANG_CODES
        logger = logging.getLogger("run")
        # scrape and store channel_id raw
        channel_raw = ChannelRawScraper.scrape(channel_id, lang_code, os)
        channel_raw.save()  # channel should be saved first
        logger.info("channel_raw saved:{}".format(str(channel_raw)))
        # scrape and store video raws (which will save caption raws)
        vid_id_list = ChannelExtractor.parse(channel_raw).vid_id_list
        vid_raw_gen = VideoRawScraper.scrape_multi(vid_id_list, channel_raw)
        for vid_idx, vid_raw in enumerate(vid_raw_gen):
            # save video_raw
            vid_raw.save()
            logger.info("video_raw saved: #{}".format(vid_idx + 1))
            # scrape and store tracks raws
            captions = CaptionExtractor.parse(vid_raw)
            tracks_raw_gen = TracksRawScraper.scrape_multi(captions)
            for track_idx, tracks_raw in enumerate(tracks_raw_gen):
                tracks_raw.save()
                logger.info("tracks_raw saved #{}".format(track_idx + 1))


class ScrapeIdiomRawsRunner(Runner):
    @classmethod
    def run(cls):
        logger = logging.getLogger("run")
        for idiom_raw in IdiomRawScraper.scrape_multi():
            idiom_raw.save()
            logger.info("idiom_raw saved:[{}]".format(str(idiom_raw)))
