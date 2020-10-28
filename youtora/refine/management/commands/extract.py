from django.core.management.base import BaseCommand, CommandError

from youtora.refine.facades import ExtractIdioms


class Command(BaseCommand):
    help = 'scrape raw data from the web'
    MODEL_NAMES = ('idiom',)

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str,
                            help="the name of the refined model to extract from raw data")

    def handle(self, *args, **options):
        model_name = options['model_name']
        if model_name not in self.MODEL_NAMES:
            raise CommandError("Not a valid model name:" + model_name)
        if model_name == self.MODEL_NAMES[0]:
            # build the general doc
            ExtractIdioms.exec()
