import re
# for breaking up long lines of text into lines of fixed width
# reference: https://stackoverflow.com/a/16320713
import textwrap

from django.core.management.base import BaseCommand
from termcolor import colored

from youtora.search.dataclasses import GeneralSrchQuery
from youtora.search.facades import SrchGeneralIdx


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
        parser.add_argument('-s', '--size', type=int,
                            help="the number of search entries to retrieve")

    def handle(self, *args, **options):
        text = options['text']
        # get the optional arguments
        capt_lang_code = options.get('capt_lang_code', None)
        chan_lang_code = options.get('chan_lang_code', None)
        size = options.get('size', None)
        # build a search query
        srch_query = GeneralSrchQuery(text, capt_lang_code=capt_lang_code,
                                      chan_lang_code=chan_lang_code, size=size)
        # do the search
        srch_results = SrchGeneralIdx.exec(srch_query)
        # print out the results
        for srch_res in srch_results:
            print("".join(["="] * self.WIDTH))
            if not srch_res.highlight:
                raise ValueError("highlight is empty")
            highlight_text = srch_res.highlight['context'][0]
            hls = self.BOLD_RE.findall(string=highlight_text)
            for hl in hls:
                highlight_text = self.BOLD_RE.sub(repl=colored(hl, 'blue'),
                                                  string=highlight_text,
                                                  # sub only the first one\
                                                  count=1)

            print(colored("context:\n", "white")
                  + textwrap.fill(highlight_text, self.WIDTH))
            print(colored("timed_url:\n", "white")
                  + srch_res.tracks[0].timed_url)
            print(colored("doc_id:\n", "white")
                  + srch_res.tracks[0].id)
