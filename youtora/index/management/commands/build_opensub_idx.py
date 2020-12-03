from django.core.management.base import BaseCommand

from youtora.index.facades import BuildOpenSubIdx


class Command(BaseCommand):
    HELP = 'build opensub_idx, from data stored in my external HDD.'

    def add_arguments(self, parser):
        parser.add_argument('splits_ndjson_dir', type=str,
                            help="The path to the directory where all ndjson splits are stored.")

    def handle(self, *args, **options):
        # build the general doc
        splits_ndjson_dir = options['splits_ndjson_dir']
        BuildOpenSubIdx.exec(splits_ndjson_dir)
