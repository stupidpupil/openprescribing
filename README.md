[![Build Status](https://travis-ci.org/ebmdatalab/openprescribing.svg?branch=master)](https://travis-ci.org/ebmdatalab/openprescribing)

Open Prescribing
================

Website code for https://openprescribing.net - a Django application that provides a REST API and dashboards for the HSCIC's [GP-level prescribing data](http://www.hscic.gov.uk/searchcatalogue?q=title%3a%22presentation+level+data%22&sort=Relevance&size=100&page=1#top)

Set up the application
======================

Set up a virtualenv
-------------------

If you're using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/):

    mkvirtualenv openprescribing
    cd openprescribing && add2virtualenv `pwd`
    workon openprescribing

Install dependencies
--------------------

Install Python dependencies in development:

    pip install -r requirements/local.txt

Or in production:

    pip install -r requirements.txt

And then install JavaScript dependencies:

    cd openprescribing/static/js
    npm install -g browserify
    npm install -g jshint
    npm install

Create database and env variables
---------------------------------

Set up a Postgres 9.4 database, with PostGIS extensions, and create a superuser for the database.

Set the `DB_NAME`, `DB_USER`, and `DB_PASS` environment variables based on the database login you used above.

You will need a `GMAIL_PASS` environment variable to send error emails in production. In development you will only need this to run tests, so you can set this to anything.

Finally set a `SECRET_KEY` environment variable (make this an SSID).

Set up the database
-------------------

Run migrations:

    python manage.py migrate

Run tests
---------

Run Django and JavaScript tests:

    make test

If required, you can run individual Django tests as follows:

    python manage.py test frontend.tests.test_api_views

Run the application
-------------------

    python manage.py runserver --settings=openprescribing.settings.local

You should now have a Django application running with no data inside it.

Load the HSCIC data
-------------------

Run setup.sh to fetch and import data, and create the indexes and materialized views needed to set up the database.

    chmod u+x setup.sh
    ./setup.sh

This is likely to take many hours to run, and will fetch more than 100GB of data. You probably want to tweak Postgres's memory settings first.

If you just want to import one month of data to get started, edit setup.sh to use `--filename` arguments (as below in 'Updating the data').

Editing JS and CSS
------------------

Source JavaScript is in `/media`, compiled JavaScript is in `/static`.

During development, run the `watch` task to see changes appear in the compiled JavaScript.

    cd openprescribing/media/js
    npm run watch

And run tests with:

    npm run test

Before deploying, run the build task to generate minified JavaScript:

    npm run build

Similarly, you can build the compiled CSS from the source LESS with:

    npm run build-css

Updating the data
-----------------

You may need to add data for new months. To do this, active your virtualenv, then wget the files you need from the HSCIC site.

You may want to start by updating organisational data, with the latest versions of the `eccg.csv` and `epraccur.csv` files:

    python manage.py import_org_names --ccg data/org_codes/eccg.csv
    python manage.py import_hscic_practices --practice_file data/raw_data/[PRACTICE FILE].CSV -v 2 --epraccur data/org_codes/epraccur.csv

If new practices were added, you may want to re-run the practice geocoder, with the latest version of the `gridall.csv` file:

    python manage.py geocode_practices -v 2 --filename data/gridall.csv

Import the chemicals:

    python manage.py import_hscic_chemicals --chem_file data/raw_data/[CHEM FILE].CSV -v 2

Then convert and import the prescribing data:

    python manage.py convert_hscic_prescribing --filename data/raw_data/[PDPI FILE].CSV -v 2
    python manage.py import_hscic_prescribing --filename data/raw_data/[PDPI FORMATTED FILE].CSV -v 2

If necessary, update list sizes for the latest months. You can get the raw list size data from the NHS BSA Information Portal:

    python manage.py import_list_sizes --filename data/list_sizes/[MONTH FILE].CSV -v 2

(If you want to add list size data for only part of a quarter, then rename the filename to cover only those months.)

Then refresh the materialized views (which will take some time, and slow the database while it runs - if doing this remotely, it's best to run this inside a screen session):

    python manage.py refresh_matviews -v 2

Now purge the CloudFlare cache and you should see the new data appear.

You may now want to run a snapshot on the DigitalOcean server, for use in backups if ever needed. This will take down the server for a few hours, so is best done in the middle of the night.

And finally, update the smoke tests in `smoke.py` - you'll need to update `NUM_RESULTS`, plus add expected values for the latest month. You can use `smoke.sh` to calculate the values you expect to see, from the raw data files.

Then re-run the smoke tests against the live data to make sure everything looks as you expect:

    python smoketests/smoke.py

Philosophy
==========

This project follows design practices from [Two Scoops of Django](http://twoscoopspress.org/products/two-scoops-of-django-1-6).