import csv
import io
import tempfile
import zipfile

import requests
from django.core.management.base import BaseCommand

from ...models import PostalCode


class Command(BaseCommand):
    help = 'Updates postalcodes from latest GeoNames database for specified countries. Can be re-run as needed.'
    base_url = 'http://download.geonames.org/export/zip/%s.zip'
    fieldnames = (
        'country_code',
        'postal_code',
        'place_name',
        'admin_name1',
        'admin_code1',
        'admin_name2',
        'admin_code2',
        'admin_name3',
        'admin_code3',
        # ignore these fields:
        # 'latitude',
        # 'longitude',
        # 'accuracy',
    )
    delimiter = '\t'

    def add_arguments(self, parser):
        parser.add_argument('country', nargs='+', type=str)

    def handle(self, *args, **options):
        for country in options['country']:
            country = country.upper()
            response = requests.get(self.base_url % country)
            zipdata = zipfile.ZipFile(io.BytesIO(response.content))
            tmpdir = tempfile.TemporaryDirectory()
            tmpfile = zipdata.extract('%s.txt' % country, path=tmpdir.name)
            for row in csv.DictReader(open(tmpfile), fieldnames=self.fieldnames, delimiter=self.delimiter):
                row.pop(None)  # remove extra fields (latitude, longitude, accuracy)
                if row['postal_code'] is None:  # must be a bogus row
                    continue
                postal_code, created = PostalCode.objects.get_or_create(
                    country_code=row.pop('country_code'),
                    postal_code=row.pop('postal_code'),
                    defaults=row,
                )
                if not created and any([getattr(postal_code, k) != v for k, v in row.items()]):
                    PostalCode.objects.filter(pk=postal_code.pk).update(**row)
            self.stdout.write(self.style.SUCCESS('Successfully updated postal codes for %s' % country))
