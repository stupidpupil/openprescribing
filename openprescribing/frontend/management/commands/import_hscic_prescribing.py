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
from frontend.models import SHA, PCT, Prescription
from common import utils


class Command(BaseCommand):
    args = ''
    help = 'Import all data from any data files that have been downloaded. '
    help += 'Set DEBUG to False in your settings before running this.'

    def add_arguments(self, parser):
        parser.add_argument('--db_name')
        parser.add_argument('--db_user')
        parser.add_argument('--db_pass')
        parser.add_argument('--filename')

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
            filepath = './data/raw_data/T*PDPI+BNFT_formatted*'
            files_to_import = glob.glob(filepath)

        for f in files_to_import:
            self.import_shas_and_pcts(f)
            self.delete_existing_prescriptions(f)
            self.import_prescriptions(f, cursor)

        self.vacuum_db(cursor)
        self.analyze_db(cursor)

        self.conn.close()

    def import_shas_and_pcts(self, filename):
        if self.IS_VERBOSE:
            print 'Importing SHAs and PCTs from %s' % filename
        rows = csv.reader(open(filename, 'rU'))
        sha_codes = set()
        pct_codes = set()
        for row in rows:
            sha_codes.add(row[0])
            pct_codes.add(row[1])
        shas_created = pcts_created = 0
        for sha_code in sha_codes:
            s, created = SHA.objects.get_or_create(code=sha_code)
            shas_created += created
        for pct_code in pct_codes:
            p, created = PCT.objects.get_or_create(code=pct_code)
            pcts_created += created
        if self.IS_VERBOSE:
            print shas_created, 'SHAs created'
            print pcts_created, 'PCTs created'

    def import_prescriptions(self, filename, cursor):
        if self.IS_VERBOSE:
            print 'Importing Prescriptions from %s' % filename
        # start = time.clock()
        copy_str = "COPY frontend_prescription(sha_id,pct_id,"
        copy_str += "practice_id,chemical_id,presentation_code,"
        copy_str += "presentation_name,total_items,net_cost,actual_cost,"
        copy_str += "quantity,processing_date,price_per_unit) FROM STDIN "
        copy_str += "WITH DELIMITER AS ','"
        file_obj = open(filename)
        cursor.copy_expert(copy_str, file_obj)
        try:
            self.conn.commit()
        except Exception as err:
            print 'EXCEPTION:', err
        # end = time.clock()
        # time_taken = (end-start)
        # print 'time_taken', time_taken

    def delete_existing_prescriptions(self, filename):
        if self.IS_VERBOSE:
            print 'Deleting existing Prescriptions for month'
        file_str = filename.split('/')[-1].split('.')[0]
        file_str = file_str.replace('PDPI+BNFT_formatted', '')
        date_from_filename = file_str[1:5] + '-' + file_str[5:] + '-01'
        p = Prescription.objects.filter(processing_date=date_from_filename)
        p.delete()

    def vacuum_db(self, cursor):
        if self.IS_VERBOSE:
            print 'Vacuuming database...'
        old_isolation_level = self.conn.isolation_level
        self.conn.set_isolation_level(0)
        cursor.execute("VACUUM frontend_prescription")
        self.conn.set_isolation_level(old_isolation_level)

    def analyze_db(self, cursor):
        if self.IS_VERBOSE:
            print 'Analyzing database...'
        cursor.execute('ANALYZE VERBOSE frontend_prescription')
