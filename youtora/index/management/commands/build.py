from django.core.management.base import BaseCommand, CommandError

from youtora.index.facades import BuildGeneralDoc


class Command(BaseCommand):
    help = 'scrape raw data from the web'
    DOC_NAMES = ('general_doc',)

    def add_arguments(self, parser):
        parser.add_argument('doc_name', type=str,
                            help='the name of the elasticsearch doc to build')

    def handle(self, *args, **options):
        doc_name = options['doc_name']
        if doc_name not in self.DOC_NAMES:
            raise CommandError("Not a valid document name:" + doc_name)
        if doc_name == self.DOC_NAMES[0]:
            # build the general doc
            BuildGeneralDoc.exec()
