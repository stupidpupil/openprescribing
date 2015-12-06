import sys
import xlrd
from django.core.management.base import BaseCommand, CommandError
from frontend.models import Practice, PCT, SHA


class Command(BaseCommand):
    args = ''
    help = 'Expects the QOF practice lookup file from WG'
    help += 'Also sets practice names and setting'

    def add_arguments(self, parser):
        parser.add_argument('--filename')

    def handle(self, *args, **options):
        self.IS_VERBOSE = False
        if options['verbosity'] > 1:
            self.IS_VERBOSE = True

        if not options['filename']:
            print('Please supply a filename')
            sys.exit()

        workbook = xlrd.open_workbook(options['filename'])
        worksheet = workbook.sheet_by_name('Practices')
        num_rows = worksheet.nrows - 1
        num_cells = worksheet.ncols - 1
        curr_row = 0

        while curr_row < num_rows:
            curr_row += 1
            row = worksheet.row(curr_row)
            code = worksheet.cell_value(curr_row, 0).strip()
            name = worksheet.cell_value(curr_row, 4).strip()
            locality_name = worksheet.cell_value(curr_row, 3).strip()
            lhb_name = worksheet.cell_value(curr_row, 1).strip()

            try:
                practice = Practice.objects.get(code=code)
                locality = PCT.objects.get(name=locality_name)
                lhb = SHA.objects.get(name=lhb_name)
                practice.name = name
                practice.ccg = locality
                practice.sha = lhb
                practice.setting = 4 #GP Practice, as unfortunately epraccur.csv identifies all Welsh practices as 0/Other
                practice.save()
            except Practice.DoesNotExist:
                pass