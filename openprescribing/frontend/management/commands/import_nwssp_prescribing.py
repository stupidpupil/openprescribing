import csv
import glob
import logging
import psycopg2
import os
import sys
import time
from pprint import pprint
from os import environ
from django.core.management.base import BaseCommand, CommandError
from frontend.models import SHA, PCT, Practice, Chemical, Prescription
from common import utils

from frontend.management.commands.import_hscic_prescribing import Command as ImportHSCICPrescribing

class Command(ImportHSCICPrescribing):
    args = ''
    help = ''

    def handle(self, *args, **options):
        self.IS_VERBOSE = False
        if options['verbosity'] > 1:
            self.IS_VERBOSE = True

        if options['db_name']:
            db_name = options['db_name']
        else:
            db_name = utils.get_env_setting('DB_NAME')
        if options['db_user']:
            db_user = options['db_user']
        else:
            db_user = utils.get_env_setting('DB_USER')
        if options['db_pass']:
            db_pass = options['db_pass']
        else:
            db_pass = utils.get_env_setting('DB_PASS')
        self.conn = psycopg2.connect(database=db_name, user=db_user,
                                     password=db_pass)
        cursor = self.conn.cursor()

        if options['filename']:
            files_to_import = [options['filename']]
        else:
            filepath = './data/nwssp_raw_data/*/GPData*_formatted*'
            files_to_import = glob.glob(filepath)

        for f in files_to_import:
            self.import_shas_and_pcts(f)
            self.delete_existing_prescriptions(f)
            self.import_prescriptions(f, cursor)

        self.vacuum_db(cursor)
        self.analyze_db(cursor)

        self.conn.close()
    

    def delete_existing_prescriptions(self, filename): #Still a horrible hack
        if self.IS_VERBOSE:
            print('Deleting existing Prescriptions for month')
        file_str = filename.split('/')[-1].split('.')[0]
        file_str = file_str.replace('GPData', '')
        file_str = file_str.replace('_formatted', '')
        date_from_filename = file_str[0:4] + '-' + file_str[4:] + '-01'
        p = Prescription.objects.filter(processing_date=date_from_filename).filter(practice__code__startswith='W')
        p.delete()