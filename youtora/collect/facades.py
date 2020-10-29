# the runners. to be accessed by django console.
import logging
import sys

from django.core.exceptions import ValidationError

from youtora.collect.scrapers import (
    ChannelRawScraper,
    VideoRawScraper,
    TracksRawScraper,
    IdiomRawScraper
)
from youtora.refine.extractors import CaptionExtractor, ChannelExtractor

# logs to standard out, logging level is at info
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class ScrapeYouTubeRaws:
    # just take out the lang codes
    LANG_CODES = [
        lang_code for lang_code, desc
        in CaptionExtractor.LANG_CODES_TO_COLLECT
    ]

    @classmethod
    def exec(cls, channel_id: str, lang_code: str, os: str = "mac"):
        """
        scrapes and saves raw data in the following order:
        1. TracksRaw
        2. VideoRaw (which includes CaptionsRaw)
        3. ChannelRaw
        channel_id raw is saved at the end.
        """
        assert lang_code in cls.LANG_CODES
        logger = logging.getLogger("exec")
        # scrape and store channel_id raw
        channel_raw = ChannelRawScraper.scrape(channel_id, lang_code, os)
        try:
            channel_raw.clean_fields()
            channel_raw.validate_unique()
        except ValidationError as ve:
            logger.warning(str(ve))
            # just pass it for now
            pass
        # just save it for now
        channel_raw.save()
        logger.info("channel_raw saved:{}".format(str(channel_raw)))
        # scrape and store video raws (which will save caption raws)
        vid_id_list = ChannelExtractor.parse(channel_raw).vid_id_list
        vid_raw_gen = VideoRawScraper.scrape_multi(vid_id_list, channel_raw.id)
        for vid_idx, vid_raw in enumerate(vid_raw_gen):
            try:
                # try validating video
                vid_raw.clean_fields()
                vid_raw.validate_unique()
            except ValidationError as ve:
                logger.warning(str(ve))
                logger.warning("SKIP:vid_raw:" + vid_raw.id)
                continue
            else:
                # this video has been validated
                vid_raw.save()
                logger.info("video_raw saved: #{}".format(vid_idx + 1))
                # scrape and store tracks raws
                captions = CaptionExtractor.parse(vid_raw)
                tracks_raw_gen = TracksRawScraper.scrape_multi(captions)
                for track_idx, tracks_raw in enumerate(tracks_raw_gen):
                    try:
                        tracks_raw.clean_fields()
                        tracks_raw.validate_unique()  # must do this before saving
                    except ValidationError as ve:
                        logger.warning(str(ve))
                        logger.warning("SKIP:tracks_raw:" + tracks_raw.id)
                        continue
                    else:
                        # this tracks_raw has been validated
                        tracks_raw.save()
                        logger.info("tracks_raw saved #{}".format(track_idx + 1))


class ScrapeIdiomRaws:
    @classmethod
    def exec(cls):
        logger = logging.getLogger("run")
        for idiom_raw in IdiomRawScraper.scrape_multi():
            idiom_raw.save()
            logger.info("idiom_raw saved:[{}]".format(str(idiom_raw)))
