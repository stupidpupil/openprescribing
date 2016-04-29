import csv
import json
import StringIO
import requests
import unittest

'''
Run smoke tests against live site. 35 separate tests to run.
Spending BY: one practice, multiple practices, one CCG,
multiple CCGs, all
Spending ON: one presentation, multiple presentations, one chemical,
multiple chemicals, one section, multiple sections, all
The expected numbers are generated from smoke.sh
'''


class SmokeTestBase(unittest.TestCase):

    DOMAIN = 'https://openprescribing.net'
    NUM_RESULTS = 65  # Should equal number of months since Aug 2010.
    NUM_RESULTS_CCG = 33 # Should equal number of months since Apr 2013.


class TestSmokeTestSpendingByEveryone(SmokeTestBase):

    def test_presentation_by_all(self):
        url = '%s/api/1.0/spending/?format=csv&' % self.DOMAIN
        url += 'code=0501013B0AAAAAA'
        r = requests.get(url)
        f = StringIO.StringIO(r.text)
        reader = csv.DictReader(f)
        all_rows = []
        for row in reader:
            all_rows.append(row)
        self.assertEqual(len(all_rows), self.NUM_RESULTS)

        expected = {
            'cost': ['173145.07', '228780.70', '207137.63', '205640.63',
                     '316925.39', '247323.08', '180616.86', '206444.12',
                     '141434.65', '122800.11', '125620.83', '118777.89',
                     '118020.47', '130835.43', '125841.77', '138486.42',
                     '158486.85', '173513.96', '164191.32', '158338.12',
                     '131714.06', '144724.09', '114181.88', '171930.90',
                     '144586.73', '138152.94', '149221.97', '139476.22',
                     '172271.70', '203581.40', '162139.09', '154016.38',
                     '176507.50', '151758.62', '131727.14', '134678.50',
                     '114468.59', '141902.17', '150113.53', '140274.34',
                     '172423.18', '177029.20', '147735.35', '148171.52',
                     '124204.42', '109308.23', '98182.55', '92726.89',
                     '78257.54', '96787.25', '112760.94', '104402.85',
                     '162214.41', '136258.51', '103858.93', '105283.89',
                     '79601.15', '67056.04', '64778.34', '56942.49',
                     '49410.42', '56696.40', '63205.95', '57609.18',
                     '69459.34'],
            'items': ['135285', '179343', '206509', '203952', '318374',
                      '246994', '179990', '205546', '157269', '134698',
                      '138143', '125593', '124433', '138858', '153877',
                      '169692', '193914', '189579', '179609', '172615',
                      '140240', '153954', '121455', '134375', '111585',
                      '108392', '151040', '141165', '176372', '178349',
                      '142975', '135271', '122785', '104976', '91230',
                      '89153', '75546', '94734', '112609', '105452',
                      '130118', '130633', '108980', '108882', '96544',
                      '83970', '75548', '69542', '58336', '73325', '81469',
                      '75573', '118616', '98160', '74280', '74828', '59537',
                      '49988', '47677', '43856', '37904', '43847', '48429',
                      '44099', '53056'],
            'quantity': ['2838007', '3749287', '4289417', '4256942', '6553681',
                         '5119893', '3733777', '4267946', '3281090', '2845359',
                         '2911772', '2644366', '2628756', '2913116', '3216317',
                         '3538889', '4041105', '3940728', '3724986', '3592338',
                         '2933496', '3215630', '2543125', '2801178', '2357189',
                         '2285574', '3156088', '2951878', '3644637', '3715441',
                         '2956887', '2806645', '2562927', '2203583', '1913688',
                         '1882929', '1599844', '1983470', '2360279', '2208527',
                         '2712684', '2729168', '2278606', '2281433', '2036425',
                         '1789562', '1608062', '1495902', '1262866', '1562048',
                         '1734820', '1609679', '2498964', '2085632', '1585963',
                         '1605846', '1301084', '1095182', '1057227', '979859',
                         '850284', '974311', '1072651', '978677', '1179054']
        }

        for i, row in enumerate(all_rows):
            self.assertEqual('%.2f' % float(row['actual_cost']), expected['cost'][i])
            self.assertEqual(row['items'], expected['items'][i])
            self.assertEqual(row['quantity'], expected['quantity'][i])

    def test_chemical_by_all(self):
        url = '%s/api/1.0/spending/?format=csv&' % self.DOMAIN
        url += 'code=0407010F0'
        r = requests.get(url)
        f = StringIO.StringIO(r.text)
        reader = csv.DictReader(f)
        all_rows = []
        for row in reader:
            all_rows.append(row)
        self.assertEqual(len(all_rows), self.NUM_RESULTS)

        expected = {
            'cost': ['6133489.35', '6595886.24', '5448794.44', '5551136.73',
                     '5837764.67', '5255731.54', '5021812.13', '5837317.50',
                     '5123377.75', '5554369.18', '5649880.60', '5385448.28',
                     '5507235.55', '5718628.68', '4763680.30', '4961449.59',
                     '5079846.80', '5245568.36', '5132817.97', '5553824.91',
                     '5224975.54', '5773668.13', '5291806.04', '7190742.14',
                     '7394035.63', '6861596.44', '6511269.10', '6424956.69',
                     '6249256.05', '6558457.36', '5890247.00', '6319251.11',
                     '6471276.30', '6728036.20', '6185170.45', '6892796.06',
                     '6695291.90', '6525265.61', '6658986.31', '6362063.89',
                     '6506565.50', '6668832.58', '5916229.32', '6448645.78',
                     '6159018.26', '6362466.30', '6109185.03', '6803242.49',
                     '6329146.77', '6704887.16', '7381763.62', '6629628.26',
                     '7417957.70', '7214341.60', '6624682.65', '7310517.54',
                     '7428270.87', '7237368.15', '7557166.49', '8451412.60',
                     '7728906.35', '8249131.33', '7575103.55', '7141302.75',
                     '7813551.53'],
            'items': ['1207416', '1298364', '1221403', '1244005', '1297529',
                      '1206699', '1144401', '1323870', '1170520', '1272598',
                      '1294637', '1234908', '1264490', '1311344', '1226903',
                      '1275021', '1289356', '1248388', '1217298', '1312834',
                      '1211848', '1333775', '1221137', '1267881', '1300668',
                      '1217327', '1300043', '1282008', '1235280', '1298413',
                      '1166055', '1245296', '1281474', '1328379', '1222904',
                      '1311318', '1271070', '1244981', '1324954', '1266266',
                      '1285570', '1322953', '1177393', '1279808', '1267123',
                      '1309035', '1260537', '1343435', '1248408', '1322880',
                      '1366847', '1229510', '1365661', '1312875', '1201278',
                      '1325698', '1296322', '1263928', '1319851', '1354201',
                      '1232839', '1330756', '1336095', '1264497', '1373827'],
            'quantity': ['132263281', '142341665', '133852506', '136440788',
                         '143503776', '131940896', '125670261', '145475520',
                         '129266366', '140284106', '142753997', '136405429',
                         '139612225', '144877361', '135203507', '140793149',
                         '143816641', '137453153', '134341747', '145254764',
                         '134279081', '148101837', '135915629', '140906059',
                         '145106910', '135375002', '144480281', '142736661',
                         '138561318', '144085272', '129382617', '138707539',
                         '142613833', '148344071', '136487586', '146719996',
                         '142620417', '138969968', '148010017', '141863575',
                         '144985723', '147761852', '131434563', '142999156',
                         '142201411', '147152477', '141312127', '151242823',
                         '140637442', '148444360', '153652249', '138268428',
                         '154635502', '147555341', '134917256', '148998685',
                         '146310229', '142783027', '149047404', '153329051',
                         '139710964', '150347699', '151134702', '143086517',
                         '156868251']
        }
        for i, row in enumerate(all_rows):
            self.assertEqual("%.2f" % float(row['actual_cost']), expected['cost'][i])
            self.assertEqual(row['items'], expected['items'][i])
            self.assertEqual(row['quantity'], expected['quantity'][i])

    def test_bnf_section_by_all(self):
        url = '%s/api/1.0/spending/?format=csv&' % self.DOMAIN
        url += 'code=0702'
        r = requests.get(url)
        f = StringIO.StringIO(r.text)
        reader = csv.DictReader(f)
        all_rows = []
        for row in reader:
            all_rows.append(row)
        self.assertEqual(len(all_rows), self.NUM_RESULTS)

        expected = {
            'cost': ['1048672.67', '1127042.93', '1042493.25', '1062209.98',
                     '988411.70', '973086.68', '990670.22', '1149901.88',
                     '969507.76', '1110820.48', '1195126.07', '1191993.85',
                     '1201804.51', '1237834.19', '1170580.04', '1244600.01',
                     '1185112.57', '1202255.45', '1169818.04', '1269828.99',
                     '1121678.15', '1282687.92', '1169826.44', '1288998.84',
                     '1305555.50', '1248961.94', '1352418.46', '1324359.56',
                     '1200235.32', '1300895.66', '1155940.37', '1276935.39',
                     '1333993.63', '1369838.44', '1318994.71', '1421618.25',
                     '1379556.61', '1357230.86', '1482408.79', '1414131.16',
                     '1397686.78', '1478486.17', '1354964.58', '1457538.12',
                     '1410476.74', '1496945.40', '1479184.18', '1574966.32',
                     '1459622.80', '1541425.02', '1610820.78', '1655841.78',
                     '1763329.16', '1746247.00', '1636268.47', '1801512.54',
                     '1719712.72', '1759283.05', '2024251.73', '2072863.43',
                     '1890817.83', '2021293.31', '2052578.68', '2002819.62',
                     '2111561.22'],
            'items': ['156561', '168362', '157446', '158295', '149587',
                      '151179', '149032', '171606', '145126', '162027',
                      '174998', '168762', '170364', '175202', '166402',
                      '176484', '165504', '169119', '163399', '177434',
                      '156048', '178286', '163706', '179681', '180437',
                      '172916', '186445', '180630', '160950', '177981',
                      '158564', '169470', '173728', '178547', '171468',
                      '184516', '177547', '176671', '187435', '177551',
                      '173461', '185364', '167303', '179236', '172467',
                      '181217', '181192', '191754', '175167', '188101',
                      '193605', '175423', '183440', '182327', '168461',
                      '186449', '177468', '176166', '189228', '193987',
                      '175902', '189147', '190828', '185440', '192420'],
            'quantity': ['3159622', '3351424', '3178985', '3271721', '3099667',
                         '2934423', '3063233', '3716267', '3203076', '3535350',
                         '3850542', '3595834', '3594433', '3750671', '3679438',
                         '3924399', '3675932', '3584288', '3547286', '3827387',
                         '3360528', '3828717', '3474576', '3729172', '3803108',
                         '3661649', '3964073', '3943316', '3573690', '3814561',
                         '3486315', '3840244', '3949773', '4060811', '3880113',
                         '4167657', '4047354', '3947199', '4302769', '4143758',
                         '4127977', '4310025', '3993760', '4305702', '4175561',
                         '4395782', '4334424', '4608948', '4274377', '4506789',
                         '4548418', '4114474', '4299903', '4234616', '4003465',
                         '4422764', '4228952', '4201360', '4451257', '4537221',
                         '4207611', '4461585', '4535819', '4413854', '4648829']
        }
        for i, row in enumerate(all_rows):
            self.assertEqual("%.2f" % float(row['actual_cost']), expected['cost'][i])
            self.assertEqual(row['items'], expected['items'][i])
            self.assertEqual(row['quantity'], expected['quantity'][i])


class TestSmokeTestSpendingByOnePractice(SmokeTestBase):

    def test_presentation_by_one_practice(self):
        url = '%s/api/1.0/spending_by_practice/?format=csv&' % self.DOMAIN
        url += 'code=0703021Q0BBAAAA&org=A81015'  # Cerazette 75mcg.
        r = requests.get(url)
        f = StringIO.StringIO(r.text)
        reader = csv.DictReader(f)
        all_rows = []
        for row in reader:
            all_rows.append(row)

        self.assertEqual(len(all_rows), self.NUM_RESULTS)

        expected = {
            'cost': ['138.94', '128.23', '77.57', '42.82', '117.64',
                     '248.45', '90.93', '173.86', '101.58', '123.08', '120.40',
                     '145.92', '197.85', '272.74', '90.98', '69.68', '206.22',
                     '109.75', '144.75', '144.80', '139.13', '166.10', '115.02',
                     '145.13', '190.37', '112.42', '198.47', '114.50', '216.49',
                     '230.51', '158.40', '153.23', '118.48', '175.15', '136.83',
                     '166.24', '110.15', '147.84', '166.75', '139.35', '191.03',
                     '145.36', '94.09', '190.16', '118.21', '126.32', '163.56',
                     '150.81', '138.92', '153.60', '103.61', '62.03', '165.33',
                     '106.48', '99.87', '117.65', '100.59', '89.03', '112.21',
                     '94.80', '76.78', '50.64', '82.91', '88.61', '76.79'],
            'items': ['16', '14', '12', '7', '13',
                      '24', '9', '17', '12', '12', '14',
                      '21', '18', '26', '12', '12', '19',
                      '10', '17', '18', '16', '16', '13',
                      '18', '20', '11', '20', '17', '22',
                      '20', '17', '16', '14', '15', '15',
                      '15', '12', '17', '19', '14', '18',
                      '17', '11', '20', '14', '13', '14',
                      '16', '13', '12', '10', '6', '14',
                      '11', '9', '10', '9', '10', '8',
                      '10', '6', '7', '8', '9', '6'],
            'quantity': ['1456', '1344', '812', '448', '1232', '2604', '952',
                         '1820', '1064', '1288', '1260', '1526', '2072',
                         '2856', '952', '728', '2156', '1148', '1512', '1512',
                         '1456', '1736', '1204', '1506', '1983', '1176',
                         '2072', '1190', '2261', '2408', '1652', '1596',
                         '1232', '1831', '1428', '1736', '1148', '1540',
                         '1736', '1456', '1995', '1512', '980', '1981', '1232',
                         '1316', '1708', '1568', '1316', '1456', '980', '588',
                         '1568', '1008', '945', '1113', '952', '840', '1064',
                         '896', '728', '476', '784', '840', '728']
        }

        for i, row in enumerate(all_rows):
            self.assertEqual("%.2f" % float(row['actual_cost']), expected['cost'][i])
            self.assertEqual(row['items'], expected['items'][i])
            self.assertEqual(row['quantity'], expected['quantity'][i])

    def test_chemical_by_one_practice(self):
        url = '%s/api/1.0/spending_by_practice/?' % self.DOMAIN
        url += 'format=csv&code=0212000AA&org=A81015'  # Rosuvastatin Calcium.
        r = requests.get(url)
        f = StringIO.StringIO(r.text)
        reader = csv.DictReader(f)
        all_rows = []
        for row in reader:
            all_rows.append(row)

        self.assertEqual(len(all_rows), self.NUM_RESULTS)

        expected = {
            'cost': ['57.22', '90.47', '57.21', '49.89', '49.92',
                     '16.63', '73.96', '57.31', '57.24', '57.32', '73.94',
                     '33.28', '90.58', '49.94', '90.56', '49.94', '81.44',
                     '33.32', '33.35',  '57.41', '57.30', '40.73', '57.28',
                     '57.38', '57.31', '56.16',  '57.29', '49.89', '83.18',
                     '98.07', '57.39', '81.50', '64.74', '97.99', '57.29',
                     '98.02', '81.38', '105.44', '57.39', '105.32', '64.72',
                     '98.06', '98.02', '98.18', '98.06', '64.80', '81.40',
                     '57.45', '81.46', '105.57', '16.68', '81.30', '125.55',
                     '84.75', '84.93', '109.11', '84.91', '109.01', '84.96',
                     '108.99', '84.89', '133.12', '84.89', '84.82', '129.05'],
            'items': ['3', '5', '3', '3', '3',
                      '1', '4', '3', '3', '3', '4',
                      '2', '5', '3', '5', '3', '4',
                      '2', '2', '3', '3', '2', '3',
                      '3', '3', '3', '3', '3', '5',
                      '5', '3', '4', '3', '5', '3',
                      '5', '4', '5', '3', '5', '3',
                      '5', '5', '5', '5', '3', '4',
                      '3', '4', '5', '1', '4', '6',
                      '4', '4', '5', '4', '5', '4',
                      '5', '4', '6', '4', '4', '6'],
            'quantity': ['84', '140', '84', '84', '84', '28', '112', '84',
                         '84', '84', '112', '56', '140', '84', '140', '84',
                         '112', '56', '56', '84', '84', '56', '84', '84',
                         '84', '82', '84', '84', '140', '140', '84', '112',
                         '84', '140', '84', '140', '112', '140', '84', '140',
                         '84', '140', '140', '140', '140', '84', '112', '84',
                         '112', '140', '28', '112', '168', '112', '112',
                         '140', '112', '140', '112', '140', '112', '168',
                         '112', '112', '168']
        }
        for i, row in enumerate(all_rows):
            self.assertEqual("%.2f" % float(row['actual_cost']), expected['cost'][i])
            self.assertEqual(row['items'], expected['items'][i])
            self.assertEqual(row['quantity'], expected['quantity'][i])

    def test_multiple_chemicals_by_one_practice(self):
        url = '%s/api/1.0/spending_by_practice/?format=csv&' % self.DOMAIN
        url += 'code=0212000B0,0212000C0,0212000M0,0212000X0,0212000Y0'
        url += '&org=C85020'  # Multiple generic statins.
        r = requests.get(url)
        f = StringIO.StringIO(r.text)
        reader = csv.DictReader(f)
        all_rows = []
        for row in reader:
            all_rows.append(row)

        self.assertEqual(len(all_rows), self.NUM_RESULTS)

        expected = {
            'cost': ['9979.53', '10289.65', '9675.42', '10249.11', '10835.87',
                     '9721.39', '9255.99', '10763.70', '9363.32', '10079.41',
                     '10457.78', '10186.81', '10481.81', '10658.54', '9891.32',
                     '11073.95', '10959.99', '9550.10', '10305.12', '11385.31',
                     '9820.74', '12811.91', '4283.13', '4285.25', '2804.97',
                     '2808.93', '2513.38', '2511.02', '2461.40', '2422.92',
                     '2225.54', '2243.14', '2458.26', '2648.84', '2269.74',
                     '2411.39', '2428.54', '2230.12', '2335.49', '2115.65',
                     '2425.06', '2274.16', '2207.01', '2322.60', '2043.00',
                     '2059.34', '1973.39', '2256.22', '2040.32', '2054.39',
                     '2316.73', '2342.52', '2042.44', '2286.73', '2527.10',
                     '2378.36', '2273.38', '2267.96', '2316.11', '2499.35',
                     '2176.26', '2259.22', '2373.20', '2291.72', '2455.49'],
            'items': ['1367', '1428', '1375', '1398', '1573',
                      '1316', '1260', '1527', '1343', '1366', '1468',
                      '1381', '1511', '1491', '1394', '1561', '1555',
                      '1454', '1530', '1601', '1459', '1895', '1788',
                      '1854', '1931', '1772', '1949', '1867', '1917',
                      '1901', '1759', '1813', '1886', '2002', '1742',
                      '1897', '1883', '1777', '1977', '1830', '2068',
                      '1945', '1812', '1826', '1871', '1867', '1809',
                      '2030', '1813', '1837', '1893', '1906', '1725',
                      '1908', '2028', '1992', '1938', '1869', '1967',
                      '2177', '1865', '2045', '2028', '2043', '2095'],
            'quantity': ['36155', '37275', '35746', '37051', '40523',
                         '34391', '32991', '39908', '35104', '35805',
                         '37996', '36057', '38750', '38633', '35422',
                         '39463', '39776', '36351', '37765', '40677',
                         '37144', '47768', '45728', '45452', '46367',
                         '44444', '46368', '45687', '47642', '46411',
                         '43201', '44506', '47102', '49260', '43185',
                         '45706', '45884', '43205', '46599', '44495',
                         '50225', '47886', '43723', '45572', '45739',
                         '46497', '44725', '49273', '44545', '44793',
                         '45512', '46728', '41358', '45988', '50549',
                         '47868', '47187', '45637', '47630', '52097',
                         '45020', '48824', '48237', '48426', '50000']
        }
        for i, row in enumerate(all_rows):
            self.assertEqual("%.2f" % float(row['actual_cost']), expected['cost'][i])
            self.assertEqual(row['items'], expected['items'][i])
            self.assertEqual(row['quantity'], expected['quantity'][i])

    def test_bnf_section_by_one_practice(self):
        url = '%s/api/1.0/spending_by_practice/' % self.DOMAIN
        url += '?format=csv&code=0304&org=L84077'
        r = requests.get(url)
        f = StringIO.StringIO(r.text)
        reader = csv.DictReader(f)
        all_rows = []
        for row in reader:
            all_rows.append(row)

        self.assertEqual(len(all_rows), self.NUM_RESULTS)

        expected = {
            'cost': ['103.89', '121.07', '257.20', '74.60', '112.71',
                     '99.62', '78.03', '219.45', '104.22', '130.93', '242.17',
                     '150.92', '261.08', '103.75', '48.54', '85.68', '70.13',
                     '105.40', '39.12', '122.96', '177.47', '110.20', '213.01',
                     '317.37', '180.87', '178.11', '97.58', '170.66', '200.57',
                     '77.88', '45.80', '153.94', '91.94', '178.93', '196.83',
                     '257.21', '194.35', '107.01', '304.33', '115.41', '76.98',
                     '136.66', '121.89', '85.19', '201.19', '148.67', '238.95',
                     '185.69', '152.56', '202.67', '166.08', '156.27', '82.07',
                     '69.95', '75.88', '123.50', '172.32', '166.42', '247.19',
                     '345.60', '193.43', '92.46', '153.58', '187.34', '114.77'],
            'items': ['37', '33', '35', '37', '36',
                      '35', '30', '50', '59', '57', '70',
                      '52', '49', '41', '20', '30', '25',
                      '28', '19', '42', '54', '66', '59',
                      '68', '50', '46', '40', '44', '45',
                      '43', '34', '46', '46', '76', '68',
                      '84', '62', '38', '55', '49', '50',
                      '59', '54', '55', '73', '73', '94',
                      '98', '73', '63', '68', '54', '60',
                      '60', '62', '60', '73', '70', '93',
                      '103', '71', '62', '59', '68', '62'],
            'quantity': ['1721', '1937', '3076', '3046', '2730', '2803',
                         '2790', '3677', '3633', '3061', '4421', '2827',
                         '2564', '2081', '711', '1581', '1262', '1549',
                         '1088', '2109', '2436', '2831', '2822', '3571',
                         '2363', '2286', '2060', '2187', '1982', '2005',
                         '1415', '2436', '1673', '3536', '3427', '4610',
                         '2742', '1823', '2007', '1484', '1528', '2058',
                         '1812', '2036', '2675', '3163', '4249', '4103',
                         '2303', '1780', '2048', '1666', '1529', '1889',
                         '2360', '2374', '3291', '2772', '4690', '3929',
                         '2834', '1915', '1667', '2240', '1646']
        }
        for i, row in enumerate(all_rows):
            self.assertEqual("%.2f" % float(row['actual_cost']), expected['cost'][i])
            self.assertEqual(row['items'], expected['items'][i])
            self.assertEqual(row['quantity'], expected['quantity'][i])


class TestSmokeTestSpendingByCCG(SmokeTestBase):

    def test_presentation_by_one_ccg(self):
        url = '%s/api/1.0/spending_by_ccg?' % self.DOMAIN
        url += 'format=csv&code=0403030E0AAAAAA&org=10Q'
        r = requests.get(url)
        f = StringIO.StringIO(r.text)
        reader = csv.DictReader(f)
        all_rows = []
        for row in reader:
            all_rows.append(row)

        self.assertEqual(len(all_rows), self.NUM_RESULTS_CCG)

        expected = {
            'cost': ['8955.03', '9104.38', '8476.08', '10254.64',
                     '10005.36', '9558.36', '9823.32', '9551.47',
                     '9913.82', '10758.87', '9798.25', '10680.19',
                     '9366.06', '9794.72', '9575.28', '10321.55',
                     '9587.88', '9874.99', '11195.18', '10139.97',
                     '11382.04', '11729.27', '10499.37', '11774.95',
                     '11617.16', '11665.55', '12136.77', '11840.51',
                     '11166.01', '11495.47', '12028.05', '11159.94',
                     '12725.15'],
            'items': ['6379', '6518', '6129', '6681', '6501',
                      '6207', '6710', '6439', '6691', '6799',
                      '6252', '6676', '6583', '6770', '6672',
                      '6949', '6470', '6741', '7142', '6490',
                      '7236', '7063', '6466', '7164', '6948',
                      '6905', '7146', '7379', '6783', '7104',
                      '7310', '6928', '7757'],
            'quantity': ['295944', '301031', '280384', '304276', '296663',
                         '283518', '305064', '296989', '307856', '310133',
                         '282511', '307581', '299143', '312277', '305538',
                         '322373', '299517', '307926', '324140', '294033',
                         '329867', '328725', '293203', '328615', '316236',
                         '317356', '330034', '335840', '317006', '326109',
                         '341404', '316559', '360994']
        }
        for i, row in enumerate(all_rows):
            self.assertEqual("%.2f" % float(row['actual_cost']), expected['cost'][i])
            self.assertEqual(row['items'], expected['items'][i])
            self.assertEqual(row['quantity'], expected['quantity'][i])

    def test_chemical_by_one_ccg(self):
        url = '%s/api/1.0/spending_by_ccg?' % self.DOMAIN
        url += 'format=csv&code=0212000AA&org=10Q'
        r = requests.get(url)
        f = StringIO.StringIO(r.text)
        reader = csv.DictReader(f)
        all_rows = []
        for row in reader:
            all_rows.append(row)

        self.assertEqual(len(all_rows), self.NUM_RESULTS_CCG)

        expected = {
            'cost': ['17191.81', '20131.86', '18143.13', '19648.75',
                     '18628.06', '19572.88', '19378.02', '19497.54',
                     '20529.77', '19686.22', '18649.07', '18896.22',
                     '20061.72', '20287.16', '20300.75', '20281.96',
                     '19749.44', '20688.56', '22274.66', '19595.64',
                     '22114.70', '22351.11', '17809.11', '21830.67',
                     '19859.25', '20254.80', '21609.31', '23332.98',
                     '19554.12', '21383.46', '21920.97', '21281.53',
                     '23784.45'],
            'items': ['715', '782', '726', '780', '752', '770', '784',
                      '773', '798', '783', '719', '769', '813', '805',
                      '820', '815', '783', '831', '891', '791', '914',
                      '915', '758', '881', '814', '842', '887', '972',
                      '850', '880', '924', '891', '981'],
            'quantity': ['25179', '29595', '26202', '28602', '26817',
                         '28332', '28396', '28335', '29148', '28841',
                         '26621', '27596', '29416', '29408', '29707',
                         '29610', '28849', '29876', '32356', '28628',
                         '32118', '32649', '26172', '31763', '28982',
                         '29802', '31621', '34209', '28566', '31221',
                         '31974', '31553', '34508']
        }
        for i, row in enumerate(all_rows):
            self.assertEqual("%.2f" % float(row['actual_cost']), expected['cost'][i])
            self.assertEqual(row['items'], expected['items'][i])
            self.assertEqual(row['quantity'], expected['quantity'][i])

    def test_bnf_section_by_one_ccg(self):
        url = '%s/api/1.0/spending_by_ccg?' % self.DOMAIN
        url += 'format=csv&code=0801&org=10Q'
        r = requests.get(url)
        f = StringIO.StringIO(r.text)
        reader = csv.DictReader(f)
        all_rows = []
        for row in reader:
            all_rows.append(row)

        self.assertEqual(len(all_rows), self.NUM_RESULTS_CCG)

        expected = {
            'cost': ['5845.77', '7588.99', '6687.19', '5756.83', '7486.50',
                     '6263.94', '5680.75', '8016.47', '7025.84', '7015.16',
                     '6785.06', '5152.56', '8115.77', '6041.56', '6775.97',
                     '8249.45', '8082.88', '8477.85', '6532.61', '7360.49',
                     '8627.81', '9020.02', '5778.31', '8132.10', '7252.01',
                     '7034.92', '7700.04', '9279.48', '8110.40', '6538.47',
                     '9935.61', '8228.91', '8478.29'],
            'items': ['206', '234', '226', '220', '208', '223', '220', '233',
                      '239', '217', '198', '207', '241', '251', '227', '224',
                      '242', '247', '232', '233', '230', '255', '209', '257',
                      '232', '247', '230', '270', '241', '236', '260', '219',
                      '262'],
            'quantity': ['11296', '13070', '11744', '10551', '11096',
                         '11002', '10812', '13557', '11838', '11173',
                         '11028', '9933', '12439', '12470', '11061',
                         '11409', '13353', '12464', '10931', '12561',
                         '12591', '12673', '11121', '11791', '11672',
                         '11666', '11693', '13638', '11946', '12640',
                         '14146', '10988', '13815']
        }
        for i, row in enumerate(all_rows):
            self.assertEqual("%.2f" % float(row['actual_cost']), expected['cost'][i])
            self.assertEqual(row['items'], expected['items'][i])
            self.assertEqual(row['quantity'], expected['quantity'][i])


class TestSmokeTestMeasures(SmokeTestBase):

    '''
    Smoke tests for all 13 KTTs, for the period July-Sept 2015.
    Cross-reference against data from the BSA site.
    NB BSA calculations are done over a calendar quarter, and ours are done
    monthly, so sometimes we have to multiply things to get the same answers.
    '''

    def get_data_for_q3_2015(self, data):
        total = {
            'numerator': 0,
            'denominator': 0
        }
        for d in data:
            if (d['date'] == '2015-07-01') or \
               (d['date'] == '2015-08-01') or \
               (d['date'] == '2015-09-01'):
               total['numerator'] += d['numerator']
               total['denominator'] += d['denominator']
        total['calc_value'] = (total['numerator'] / float(total['denominator'])) * 100
        return total

    def retrieve_data_for_measure(self, measure, practice):
        self.DOMAIN = 'http://localhost:8000'
        url = '%s/api/1.0/measure_by_practice/?format=json&' % self.DOMAIN
        url += 'measure=%s&org=%s' % (measure, practice)
        r = requests.get(url)
        data = json.loads(r.text)
        rows = data['measures'][0]['data']
        return self.get_data_for_q3_2015(rows)

    def test_measure_by_practice(self):
        q = self.retrieve_data_for_measure('ktt3_lipid_modifying_drugs', 'A81001')
        bsa = {
            'numerator': 34,
            'denominator': 1265,
            'calc_value': '2.688'
        }
        self.assertEqual(q['numerator'], bsa['numerator'])
        self.assertEqual(q['denominator'], bsa['denominator'])
        self.assertEqual("%.3f" % q['calc_value'], bsa['calc_value'])

        q = self.retrieve_data_for_measure('ktt8_antidepressant_first_choice', 'A81001')
        bsa = {
            'numerator': 643,
            'denominator': 1025,
            'calc_value': '62.732'
        }
        self.assertEqual(q['numerator'], bsa['numerator'])
        self.assertEqual(q['denominator'], bsa['denominator'])
        self.assertEqual("%.3f" % q['calc_value'], bsa['calc_value'])

        q = self.retrieve_data_for_measure('ktt8_dosulepin', 'A81001')
        bsa = {
            'numerator': 24,
            'denominator': 1025,
            'calc_value': '2.341'
        }
        self.assertEqual(q['numerator'], bsa['numerator'])
        self.assertEqual(q['denominator'], bsa['denominator'])
        self.assertEqual("%.3f" % q['calc_value'], bsa['calc_value'])

        q = self.retrieve_data_for_measure('ktt9_antibiotics', 'A81001')
        bsa = {
            'numerator': 577,
            'denominator': 7581.92, # BSA's actual STAR-PU value is 7509
            'calc_value': (577 / 7581.92) * 100
        }
        self.assertEqual(q['numerator'], bsa['numerator'])
        self.assertEqual("%.0f" % q['denominator'], "%.0f" % bsa['denominator'])
        self.assertEqual("%.2f" % q['calc_value'], "%.2f" % bsa['calc_value'])

        q = self.retrieve_data_for_measure('ktt9_cephalosporins', 'A81001')
        bsa = {
            'numerator': 30,
            'denominator': 577,
            'calc_value': '5.199'
        }
        self.assertEqual(q['numerator'], bsa['numerator'])
        self.assertEqual(q['denominator'], bsa['denominator'])
        self.assertEqual("%.3f" % q['calc_value'], bsa['calc_value'])

        q = self.retrieve_data_for_measure('ktt10_uti_antibiotics', 'A81001')
        bsa = {
            'numerator': 579.833,
            'denominator': 72,
            'calc_value': '8.053'
        }
        self.assertEqual("%.3f" % q['numerator'], str(bsa['numerator']))
        self.assertEqual(q['denominator'], bsa['denominator'])
        # Note that BSA divides the value by 100, for no obvious reason.
        self.assertEqual("%.3f" % (q['calc_value'] / 100), bsa['calc_value'])

        # Note practice A81005, as A81001 does not appear in published data
        q = self.retrieve_data_for_measure('ktt11_minocycline', 'A81006')
        bsa = {
            'numerator': 28,
            'denominator': 12.235 * 3,
            'calc_value': (28 / (12.235 * 3)) * 100
        }
        self.assertEqual(q['numerator'], bsa['numerator'])
        self.assertEqual(q['denominator'], bsa['denominator'])
        self.assertEqual("%.2f" % q['calc_value'], "%.2f" % bsa['calc_value'])

        q = self.retrieve_data_for_measure('ktt12_diabetes_blood_glucose', 'A81001')
        bsa = {
            'numerator': 543,
            'denominator': 626,
            'calc_value': '86.741'
        }
        self.assertEqual(q['numerator'], bsa['numerator'])
        self.assertEqual(q['denominator'], bsa['denominator'])
        self.assertEqual("%.3f" % q['calc_value'], bsa['calc_value'])

        q = self.retrieve_data_for_measure('ktt12_diabetes_insulin', 'A81001')
        bsa = {
            'numerator': 44,
            'denominator': 64,
            'calc_value': '68.750'
        }
        self.assertEqual(q['numerator'], bsa['numerator'])
        self.assertEqual(q['denominator'], bsa['denominator'])
        self.assertEqual("%.3f" % q['calc_value'], bsa['calc_value'])

        q = self.retrieve_data_for_measure('ktt13_nsaids_ibuprofen', 'A81001')
        bsa = {
            'numerator': 356,
            'denominator': 413,
            'calc_value': '86.199'
        }
        self.assertEqual(q['numerator'], bsa['numerator'])
        self.assertEqual(q['denominator'], bsa['denominator'])
        self.assertEqual("%.3f" % q['calc_value'], bsa['calc_value'])

    def test_measure_by_ccg(self):
        pass

if __name__ == '__main__':
    unittest.main()
