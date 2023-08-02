from django.core.management.base import BaseCommand
from observations.get_data import get_data


class Command(BaseCommand):
    help = 'Retrieves new data from the Sensor.Community API'

    def handle(self, *args, **options):
        get_data()
