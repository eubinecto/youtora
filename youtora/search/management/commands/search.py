import re
# for breaking up long lines of text into lines of fixed width
# reference: https://stackoverflow.com/a/16320713
import textwrap

from django.core.management.base import BaseCommand
from termcolor import colored

from youtora.search.dataclasses import SrchQuery
from youtora.search.facades import SrchGeneralDoc


class Command(BaseCommand):
    help = 'search and print out the result for a given text'
    BOLD_RE = re.compile(r'<strong>([\S ]+?)</strong>')
    WIDTH = 60

    def add_arguments(self, parser):
        parser.add_argument('text', type=str, help='the text to search on general_doc')

    def handle(self, *args, **options):
        text = options['text']
        # build a search query
        srch_query = SrchQuery(text)
        # do the search
        srch_results = SrchGeneralDoc.exec(srch_query)
        # print out the results
        for srch_res in srch_results:
            print("".join(["="] * self.WIDTH))
            hls = self.BOLD_RE.findall(string=srch_res.highlight)
            for idx, hl in enumerate(hls):
                srch_res.highlight = self.BOLD_RE.sub(repl=colored(hl, 'blue'),
                                                      string=srch_res.highlight,
                                                      count=idx + 1)
            print(textwrap.fill(srch_res.highlight, self.WIDTH))
            print(srch_res.tracks[0].timed_url)
