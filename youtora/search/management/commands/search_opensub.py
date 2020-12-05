import re

from django.core.management.base import BaseCommand

from youtora.search.dataclasses import OpensubSrchQuery


# for breaking up long lines of text into lines of fixed width
# reference: https://stackoverflow.com/a/16320713


class Command(BaseCommand):
    help = 'search and print out the result for a given text'
    BOLD_RE = re.compile(r'<strong>([\S ]+?)</strong>')
    WIDTH = 60

    def add_arguments(self, parser):
        parser.add_argument('text', type=str, help='the text to search on opensub_idx')
        # optional arguments
        parser.add_argument('-s', '--size', type=int,
                            help="the number of search entries to retrieve")

    def handle(self, *args, **options):
        text = options['text']
        # get the optional arguments
        size = options.get('size', None)
        # build a search query
        srch_query = OpensubSrchQuery(text=text,
                                      size=size)
