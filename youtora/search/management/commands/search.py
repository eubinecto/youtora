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
        # optional arguments
        parser.add_argument('-captl', '--capt_lang_code', type=str,
                            help="the language of the caption")
        parser.add_argument('-chanl', '--chan_lang_code', type=str,
                            help="the language of the channel")

    def handle(self, *args, **options):
        text = options['text']
        capt_lang_code = options.get('capt_lang_code', None)
        chan_lang_code = options.get('chan_lang_code', None)
        # build a search query
        srch_query = SrchQuery(text,
                               capt_lang_code=capt_lang_code,
                               chan_lang_code=chan_lang_code)
        # do the search
        srch_results = SrchGeneralDoc.exec(srch_query)
        # print out the results
        for srch_res in srch_results:
            print("".join(["="] * self.WIDTH))
            hls = self.BOLD_RE.findall(string=srch_res.highlight)
            for hl in hls:
                srch_res.highlight = self.BOLD_RE.sub(repl=colored(hl, 'blue'),
                                                      string=srch_res.highlight,
                                                      # sub only the first one\
                                                      count=1)

            print(colored("context:\n", "white")
                  + textwrap.fill(srch_res.highlight, self.WIDTH))
            print(colored("timed_url:\n", "white")
                  + srch_res.tracks[0].timed_url)
            print(colored("doc_id:\n", "white")
                  + srch_res.tracks[0].id)
