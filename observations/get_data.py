from datetime import datetime

import pytz
import requests
from django.utils.timezone import make_aware

from observations.models import Sensor, Observation

TYPE_MAP = {
    'P1': 'pm10',
    'P2': 'pm25',
    'temperature': 'temp',
    'humidity': 'rh',
}

def get_data():
    response = requests.get('https://data.sensor.community/static/v2/data.json')
    response_data = response.json()

    country_filtered_data = filter_country(response_data, country_code='NL')
    add_sensors(country_filtered_data)


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
        timestamp = make_aware(datetime.strptime(row['timestamp'], '%Y-%m-%d %H-%M-%S'), pytz.timezone('UTC'))

        for observation_data in row:
            observation_type = TYPE_MAP.get(observation_data['value_type'])

            if observation_type is None:
                continue

            observations.append(
                Observation(
                    timestamp=timestamp,
                    type=observation_type,
                    value=float(observation_data['value']),
                    sensor=Sensor.objects.get(sensor_community_id=int(row['sensor']))
                )
            )

    Observation.objects.bulk_create(observations)


def filter_country(data, country_code='NL'):
    return [row for row in data if row['location']['country'] == country_code]
