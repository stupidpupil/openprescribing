import csv
import sys
from django.core.management.base import BaseCommand, CommandError
from frontend.models import Practice, PCT, SHA


class Command(BaseCommand):
    args = ''
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('--filename')

    def handle(self, *args, **options):
        if not options['filename']:
            options['filename'] = './data/org_codes/welsh_lhbs.csv'

        entries = csv.reader(open('%s' % options['filename'], 'rU'))
        for row in entries:
            row = [i.strip() for i in row]
            lhb, created = SHA.objects.get_or_create(code=row[0])
            lhb.name = row[1]
            lhb.save()