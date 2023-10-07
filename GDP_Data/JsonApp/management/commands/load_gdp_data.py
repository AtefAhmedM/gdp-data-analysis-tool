import json
from django.core.management.base import BaseCommand
from JsonApp.models import YourModel

class Command(BaseCommand):
    help = 'Load GDP data from a JSON file into the database'

    def handle(self, *args, **options):
        try:
            with open('JsonData.json', 'r') as file:
                json_data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('JSON file not found.'))
            return

        YourModel.objects.all().delete()  # Clear existing data

        for item in json_data:
            YourModel.objects.create(
                country_name=item['country_name'],
                year=item['year'],
                gdp_value=item['value'],
                gdp_growth=0  # You can set this to your desired value
            )

        self.stdout.write(self.style.SUCCESS('GDP data loaded successfully.'))
