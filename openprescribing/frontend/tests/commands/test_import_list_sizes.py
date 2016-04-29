from django.core.management import call_command
from django.test import TestCase
from frontend.models import Practice, PracticeStatistics


def setUpModule():
        Practice.objects.create(code='N84014',
                                name='AINSDALE VILLAGE SURGERY')
        Practice.objects.create(code='P84034',
                                name='BARLOW MEDICAL CENTRE')
        Practice.objects.create(code='Y02229',
                                name='ADDACTION NUNEATON')


def tearDownModule():
    call_command('flush', verbosity=0, interactive=False)


class CommandsTestCase(TestCase):
    def test_import_bsa_list_size_quarterly(self):

        args = []
        fname = 'frontend/tests/fixtures/commands/'
        fname += 'Patient_List_Size_2013_10-12.csv'
        opts = {
            'filename': fname
        }
        call_command('import_list_sizes', *args, **opts)

        list_sizes = PracticeStatistics.objects.all()
        self.assertEqual(len(list_sizes), 9)

        p = PracticeStatistics.objects.get(practice_id='N84014',
                                           date='2013-10-01')
        self.assertEqual(p.total_list_size, 2932)
        self.assertEqual(p.astro_pu_cost, 12358.6840999993)
        self.assertEqual(p.astro_pu_items, 45377.5747635734)
        self.assertEqual('%.3f' % p.star_pu['oral_antibacterials_item'],
                         '1764.245')
        self.assertEqual('%.3f' % p.star_pu['cox-2_inhibitors_cost'],
                         '968.672')
        self.assertEqual('%.3f' % p.star_pu['antidepressants_adq'],
                         '66516.700')
        for k in p.star_pu:
            self.assertNotEqual(p.star_pu[k], 0)
            self.assertNotEqual(p.star_pu[k], None)

        # Test that our script creates all months in the quarter.
        p = PracticeStatistics.objects.get(practice_id='N84014',
                                           date='2013-11-01')
        self.assertEqual(p.total_list_size, 2932)
        self.assertEqual(p.astro_pu_cost, 12358.6840999993)
        self.assertEqual(p.astro_pu_items, 45377.5747635734)
        self.assertEqual('%.3f' % p.star_pu['oral_antibacterials_item'],
                         '1764.245')
        self.assertEqual('%.3f' % p.star_pu['cox-2_inhibitors_cost'],
                         '968.672')
        self.assertEqual('%.3f' % p.star_pu['antidepressants_adq'],
                         '66516.700')

        p = PracticeStatistics.objects.get(practice_id='N84014',
                                           date='2013-12-01')
        self.assertEqual(p.total_list_size, 2932)
        self.assertEqual(p.astro_pu_cost, 12358.6840999993)
        self.assertEqual(p.astro_pu_items, 45377.5747635734)
        self.assertEqual('%.3f' % p.star_pu['oral_antibacterials_item'],
                         '1764.245')
        self.assertEqual('%.3f' % p.star_pu['cox-2_inhibitors_cost'],
                         '968.672')
        self.assertEqual('%.3f' % p.star_pu['antidepressants_adq'],
                         '66516.700')

        p = PracticeStatistics.objects.get(practice_id='P84034',
                                           date='2013-12-01')
        self.assertEqual(p.total_list_size, 13439)
        self.assertEqual(p.astro_pu_cost, 41303.5675254791)
        self.assertEqual(p.astro_pu_items, 144028.821414122)
        self.assertEqual('%.3f' % p.star_pu['oral_antibacterials_item'],
                         '7100.005')
        self.assertEqual('%.3f' % p.star_pu['cox-2_inhibitors_cost'],
                         '3287.111')
        self.assertEqual('%.3f' % p.star_pu['antidepressants_adq'],
                         '295093.300')

        p = PracticeStatistics.objects.get(practice_id='Y02229',
                                           date='2013-12-01')
        self.assertEqual(p.total_list_size, 0)
        self.assertEqual(p.astro_pu_cost, 0)
        self.assertEqual(p.astro_pu_items, 0)
        self.assertEqual(p.star_pu['oral_antibacterials_item'], 0)
        self.assertEqual(p.star_pu['cox-2_inhibitors_cost'], 0)
        self.assertEqual(p.star_pu['antidepressants_adq'], 0)

    def test_import_foi_file(self):

        # Test that the FOI file, with an explicit 'Month' field
        # rather than months in the filename, also loads correctly.
        args = []
        fname = 'frontend/tests/fixtures/commands/'
        fname += 'Patient_List_Size_nodate.csv'
        opts = {
            'filename': fname
        }
        call_command('import_list_sizes', *args, **opts)

        p = PracticeStatistics.objects.get(practice_id='P84034',
                                           date='2011-04-01')
        self.assertEqual(p.total_list_size, 12842)
        self.assertEqual(p.astro_pu_cost, 39098.6573715275)
        self.assertEqual(p.astro_pu_items, 136780.949819498)

        p = PracticeStatistics.objects.get(practice_id='P84034',
                                           date='2011-05-01')
        self.assertEqual(p.total_list_size, 12842)
        self.assertEqual(p.astro_pu_cost, 39098.6573715275)
        self.assertEqual(p.astro_pu_items, 136780.949819498)

        p = PracticeStatistics.objects.get(practice_id='P84034',
                                           date='2011-06-01')
        self.assertEqual(p.total_list_size, 12842)
        self.assertEqual(p.astro_pu_cost, 39098.6573715275)
        self.assertEqual(p.astro_pu_items, 136780.949819498)
