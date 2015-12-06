import os
import urllib.request
import re
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = ''
    help = 'Downloads all GP Data Extracts found on the NWSSP Primary Care Services site'
    help += 'Requires 7za for extraction'

    def handle(self, *args, **options):
        links = self.fetch_list_of_gp_data_extracts()

        print("%d GP Data Extracts found" % len(links))
        for l in links:
            url = ("http://www.primarycareservices.wales.nhs.uk/opendoc/%s" % l[0])
            dir_path = ("./data/nwssp_raw_data/%s - %s" % (l[0],l[1]))
            zip_path = ("%s.zip" % dir_path)
            self.download_gp_data_extract(url, zip_path)
            self.unzip_gp_data_extract(zip_path, dir_path)

    def fetch_list_of_gp_data_extracts(self):
        url = 'http://www.primarycareservices.wales.nhs.uk/general-practice-prescribing-data-extrac'
        link_regex = re.compile('<a class="doclink" href="opendoc/(\d+?)" title="Download GP Data Extract - (.+?) \(GP Prescribing Data Extract\)">', re.IGNORECASE)

        with urllib.request.urlopen(url) as response:
            links = link_regex.findall(response.read().decode('utf-8'))

        return links

    def download_gp_data_extract(self, url, path):
        print("Downloading %s" % url)
        urllib.request.urlretrieve(url, path)

    def unzip_gp_data_extract(self, zip_path, dir_path):
        print("Unzipping %s" % zip_path)
        zip_command = '7za x "%s" -o"%s"' % (zip_path, dir_path)
        return os.system(zip_command)
