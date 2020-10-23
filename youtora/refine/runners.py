import logging
import sys

from youtora.collect.models import IdiomRaw
from youtora.refine.extractors import IdiomExtractor

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class ExtractIdiomsRunner:
    @classmethod
    def run(cls):
        logger = logging.getLogger("run")
        # get all idiom raws
        idiom_raw_gen = IdiomRaw.objects.all()
        idiom_gen = (
            IdiomExtractor.parse(idiom_raw)
            for idiom_raw in idiom_raw_gen
        )
        # save each idiom
        for idx, idiom in enumerate(idiom_gen):
            idiom.save()
            logger.info("idiom saved: #{}".format(idx + 1))
