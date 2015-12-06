import csv
import glob
import sys
from django.core.management.base import BaseCommand, CommandError
from frontend.models import Practice

from frontend.management.commands.import_hscic_practices import Command as ImportHSCICPractices

class Command(ImportHSCICPractices):
    args = ''
    help = ''

    def handle(self, *args, **options):
        self.IS_VERBOSE = False
        if options['verbosity'] > 1:
            self.IS_VERBOSE = True

        if options['practice_file']:
            practice_files = [options['practice_file']]
        else:
            practice_files = glob.glob('./data/nwssp_raw_data/*/Address.csv')
        for f in practice_files:
            self.import_practices(f)

    def import_practices(self, filename):
        if self.IS_VERBOSE:
            print('Importing practices from %s' % filename)
        lines = count = 0
        practices = csv.reader(open(filename, 'rU'))
        for row in practices:

            row = [i.strip() for i in row]

            if(len(row[1]) != 6):
                continue

            p, created = Practice.objects.get_or_create(
                code=row[1]
            )
            p.name = row[2]
            p.address1 = row[3]
            p.address2 = row[4]
            p.address3 = row[5]
            p.address4 = row[6]
            p.postcode = row[7]
            p.save()
            lines += 1
            if created:
                count += 1
        if self.IS_VERBOSE:
            print('%s lines read, %s Practice objects created' % (lines, count))