# for breaking up long lines of text into lines of fixed width
# reference: https://stackoverflow.com/a/16320713  # refer to this later, for printing out results.
import textwrap

from django.core.management.base import BaseCommand

from youtora.search.builders import GeneralSrchQueryBuilder, GeneralSrchResBuilder
from youtora.search.facades import SrchFacade


class Command(BaseCommand):
    help = 'search the given text on general_idx'
    WIDTH = 60

    def add_arguments(self, parser):
        parser.add_argument('text', type=str, help='the text to search on general_doc')
        # optional arguments
        parser.add_argument('-captl', '--capt_lang_code', type=str, default=None,
                            help="the language of the caption")
        parser.add_argument('-chanl', '--chan_lang_code', type=str, default=None,
                            help="the language of the channel")
        parser.add_argument('-f', '--from', type=int, default=0,
                            help="from which entry?")
        parser.add_argument('-s', '--size', type=int, default=20,
                            help="the number of search entries to retrieve")

    def handle(self, *args, **options):
        # get the optional arguments
        params = {
            'text': options['text'],
            'capt_lang_code': options['capt_lang_code'],
            'chan_lang_code': options['chan_lang_code'],
            'from_': options['from'],
            'size': options['size']
        }
        # build a search query with the given params
        srch_q_builder = GeneralSrchQueryBuilder(**params)
        srch_facade = SrchFacade(srch_q_builder,
                                 srch_r_builder_type=GeneralSrchResBuilder)
        srch_res = srch_facade.exec()
        for entry in srch_res.entries:
            # we know that we have three tracks... and highlight.
            prev_timed_url = entry['tracks'][0]['timed_url']
            highlight_text = entry['highlight']['text']
            wrapped_text = textwrap.fill(highlight_text, width=self.WIDTH)
            print(wrapped_text)
            print(prev_timed_url)
            print("##############")  # this should work.. hopefully.
