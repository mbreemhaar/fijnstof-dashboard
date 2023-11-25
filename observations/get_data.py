from datetime import datetime, timedelta

import requests
from django.utils.timezone import make_aware, now

from observations.models import Sensor, Observation

TYPE_MAP = {
    'P1': 'pm10',
    'P2': 'pm25',
    'temperature': 'temp',
    'humidity': 'rh',
}


def get_data():
    print('Retrieving data from Sensor Community API...')
    response = requests.get('https://data.sensor.community/static/v2/data.json')
    response_data = response.json()

    print('Filtering out all data from non-Dutch sensors...')
    country_filtered_data = filter_country(response_data, country_code='NL')

    print('Adding new sensors to database...')
    add_sensors(country_filtered_data)

    print('Writing observations to database...')
    add_observations(country_filtered_data)

    print('Removing old observations from database...')
    delete_old_observations()

    print('Done!')


def add_sensors(data):
    for row in data:
        Sensor.objects.get_or_create(
            sensor_community_id=int(row['sensor']['id']),
            defaults={
                'latitude': row['location']['latitude'],
                'longitude': row['location']['longitude'],
            }
        )


def add_observations(data):
    observations = []
    for row in data:
        timestamp = make_aware(datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S'))

        for observation_data in row['sensordatavalues']:
            observation_type = TYPE_MAP.get(observation_data['value_type'])

            if observation_type is None:
                continue

            value = round(float(observation_data['value']), 3)
            if value > 999:
                continue

            if observation_type == 'temp' and (value < -60 or value > 60):
                continue

            if observation_type == 'rh' and (value < 0 or value > 100):
                continue

            observations.append(
                Observation(
                    timestamp=timestamp,
                    type=observation_type,
                    value=value,
                    sensor=Sensor.objects.get(sensor_community_id=int(row['sensor']['id']))
                )
            )

    Observation.objects.bulk_create(observations)


def delete_old_observations(delta=timedelta(minutes=15)):
    Observation.objects.filter(timestamp__lt=now()-delta).delete()


def delete_old_sensors():
    Sensor.objects.filter(observation__isnull=True).delete()


def filter_country(data, country_code='NL'):
    return [row for row in data if row['location']['country'] == country_code]
