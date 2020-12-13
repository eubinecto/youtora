import re
import textwrap

from django.core.management.base import BaseCommand

from youtora.search.builders import OpensubSrchQueryBuilder, OpensubResEntryBuilder
from youtora.search.facades import SrchFacade


class Command(BaseCommand):
    help = 'search and print out the result for a given text'
    BOLD_RE = re.compile(r'<strong>([\S ]+?)</strong>')
    WIDTH = 60

    def add_arguments(self, parser):
        parser.add_argument('text', type=str, help='the text to search on opensub_idx')
        # optional
        parser.add_argument('-f', '--from', type=int, default=0,
                            help="from which entry?")
        parser.add_argument('-s', '--size', type=int, default=10,
                            help="the number of search entries to retrieve")

    def handle(self, *args, **options):
        params = {
            'text': options['text'],
            'from_': options['from'],
            'size': options['size']
        }
        # build a search query with the given params.
        srch_q_builder = OpensubSrchQueryBuilder()
        srch_q_builder.prep(**params)
        res_e_builder = OpensubResEntryBuilder()
        srch_facade = SrchFacade(srch_q_builder, res_e_builder)
        srch_res = srch_facade.exec()
        for entry in srch_res.entries:
            # we know that we have three tracks... and highlight.
            highlight_text = entry.body['highlight']['text']
            wrapped_text = textwrap.fill(highlight_text, width=self.WIDTH)
            print(wrapped_text)
            print("#############")
