import csv
import glob
from django.core.management.base import BaseCommand, CommandError

from frontend.management.commands.convert_hscic_prescribing import Command as ConvertHSCICPrescribing

class Command(ConvertHSCICPrescribing):

    def handle(self, *args, **options):
        self.IS_VERBOSE = False
        if options['verbosity'] > 1:
            self.IS_VERBOSE = True

        if 'is_test' in options:
            self.IS_TEST = True
        else:
            self.IS_TEST = False

        if options['filename']:
            filenames = [options['filename']]
        else:
            filenames = glob.glob('./data/nwssp_raw_data/*/GPData*.csv')

        for f in filenames:
            if self.IS_VERBOSE:
                print("--------- Converting %s -----------" % f)
            reader = csv.reader(open(f, 'rU'))
            next(reader)
            filename_for_output = self.create_filename_for_output_file(f)
            writer = csv.writer(open(filename_for_output, 'w'))
            for row in reader:
                if(len(row[2].strip()) !=  6):
                    continue

                data = self.format_row_for_sql_copy(row)
                writer.writerow(data)

    def get_chemical_id(self, presentation_id):
        return presentation_id[:9] #HACK, to work with NWSSP chemicals
