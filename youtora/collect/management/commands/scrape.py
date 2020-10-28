from django.core.management.base import BaseCommand, CommandError

from youtora.collect.facades import ScrapeYouTubeRaws, ScrapeIdiomRaws


class Command(BaseCommand):
    help = 'scrape raw data from the web'
    RAW_TYPES = ('youtube', 'idiom')

    def add_arguments(self, parser):
        parser.add_argument('raw_type', type=str,
                            help='the type of raw data to scrape')

        # optional arguments
        parser.add_argument('-c', '--channel_id', type=str,
                            help="the channel id of the channel to be scraped")
        parser.add_argument('-l', '--lang_code', type=str,
                            help="the language of the channel")

    def handle(self, *args, **options):
        raw_type = options['raw_type']
        if raw_type not in self.RAW_TYPES:
            raise CommandError("Not a valid raw type:" + raw_type)
        if raw_type == self.RAW_TYPES[0]:
            # scrape youtube raws
            channel_id = options['channel_id']
            lang_code = options['lang_code']
            if not channel_id or not lang_code:
                raise CommandError("for scraping a channel, both"
                                   "channel_id (-c) and lang_code (-l) must be given")
            ScrapeYouTubeRaws.exec(channel_id, lang_code)
        elif raw_type == self.RAW_TYPES[1]:
            # scrape idiom raws
            ScrapeIdiomRaws.exec()
