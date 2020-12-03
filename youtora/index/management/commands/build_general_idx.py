from django.core.management.base import BaseCommand

from youtora.index.facades import BuildGeneralIdx


class Command(BaseCommand):
    HELP = 'build general_idx, from the data stored in youtora_db'

    def add_arguments(self, parser):
        parser.add_argument('-c', '--channel_id', type=str,
                            help="the id of the channel to build documents for."
                                 "if this is not given, all channels will be indexed.")

    def handle(self, *args, **options):
        # build the general doc
        channel_id = options['channel_id']
        if not channel_id:
            BuildGeneralIdx.exec_multi()
        else:
            BuildGeneralIdx.exec(channel_id)
