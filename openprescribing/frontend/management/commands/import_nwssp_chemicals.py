import csv
import glob
import sys
from django.core.management.base import BaseCommand, CommandError
from frontend.models import Practice

from frontend.management.commands.import_hscic_chemicals import Command as ImportHSCICChemicals

class Command(ImportHSCICChemicals):
    def handle(self, *args, **options):
        self.IS_VERBOSE = False
        if options['verbosity'] > 1:
            self.IS_VERBOSE = True

        self.import_missing_chemicals()

        if options['chem_file']:
            chem_files = [options['chem_file']]
        else:
            chem_files = glob.glob('./data/nwssp_raw_data/*/ChemSubstance.csv')
        for f in chem_files:
            self.import_chemicals(f)

    def import_chemicals(self, filename):
        if self.IS_VERBOSE:
            print('Importing Chemicals from %s' % filename)
        lines = count = 0
        chemicals = csv.DictReader(open(filename, 'rU'))
        for row in chemicals:
            row = self._strip_dict(row)
            bnf_code = row['BNFChemical']
            if '+' in bnf_code:
                print('ERROR in BNF code format:', bnf_code)
                print('In file:', filename)
                sys.exit()
            c, created = Chemical.objects.get_or_create(
                bnf_code=bnf_code
            )
            c.chem_name = row['Chemical']
            c.save()
            lines += 1
            count += created
        if self.IS_VERBOSE:
            print('%s lines read, %s Chemical objects created' % (lines, count))