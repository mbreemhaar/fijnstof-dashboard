import requests

from observations.models import Sensor


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


def filter_country(data, country_code='NL'):
    return [row for row in data if row['location']['country'] == country_code]
