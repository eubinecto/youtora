from django.core.management.base import BaseCommand, CommandError

from youtora.index.docs import GeneralDoc
from youtora.index.facades import BuildGeneralIdx


class Command(BaseCommand):
    HELP = 'scrape raw data from the web'
    IDX_NAMES = [GeneralDoc.Index.name]

    def add_arguments(self, parser):
        parser.add_argument('idx_name', type=str,
                            help='the name of the elasticsearch idx to build')

        parser.add_argument('-c', '--channel_id', type=str,
                            help="the id of the channel to build documents for")

    def handle(self, *args, **options):
        idx_name = options['idx_name']
        if idx_name not in self.IDX_NAMES:
            raise CommandError("Not a valid document name:" + idx_name)
        if idx_name == self.IDX_NAMES[0]:
            # build the general doc
            channel_id = options['channel_id']
            if not channel_id:
                BuildGeneralIdx.exec_multi()
            else:
                BuildGeneralIdx.exec(channel_id)
