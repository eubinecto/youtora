import logging
from sys import stdout

from django.core.management import BaseCommand

from youtora.index.docs import GeneralDoc, OpenSubDoc

logging.basicConfig(stream=stdout, level=logging.INFO)


class Command(BaseCommand):
    HELP = 'migrate index mappings to elasticsearch'

    def handle(self, *args, **options):
        logger = logging.getLogger("handle")
        GeneralDoc.init()
        OpenSubDoc.init()
        logger.info("migration successful")
