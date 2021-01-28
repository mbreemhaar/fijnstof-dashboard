import requests
import pandas as pd
import sys
import os
import datetime
from progress.bar import IncrementalBar

def get_last_observation(sensor, observation_type):
    datastream_link = sensor['Datastreams@iot.navigationLink']
    datastream_request = requests.get(datastream_link + "?$filter=endswith(name, '{}')".format(observation_type))

    try:
        observation_link = datastream_request.json()['value'][0]['Observations@iot.navigationLink']
        observation_request = requests.get(observation_link + '?$top=1&$select=result,phenomenonTime')
    except IndexError:
        return None

    try:
        observation_result = observation_request.json()['value'][0]['result']
        observation_date = observation_request.json()['value'][0]['phenomenonTime']
    except IndexError:
        return None
    
    return observation_result, observation_date

def update_observation_dict(observation_dict, sensor, observation_type):
    observation = get_last_observation(sensor, observation_type)
    if observation:
        observation_dict[observation_type] = observation[0]
        observation_dict['date'] = observation[1]

    return observation_dict

def make_output_dir(filename):
    # Create output directory at script location
    script_dir = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(os.path.join(script_dir, filename)):
        os.mkdir(os.path.join(script_dir, filename))

    return os.path.join(script_dir, filename)

def get_province_municipality_codes(province_code_list):
    # Get municipality codes of all province
    municipalities = pd.read_csv(os.path.join('gemeenten-alfabetisch-2021.csv'))
    filtered_municipalities = municipalities[municipalities.Provinciecode.isin(province_code_list)]
    return filtered_municipalities['Gemeentecode']

def get_sensors_in_municipalities(municipality_code_list, filter_project=None):
    # Generate query filter string for municipalities
    filter_query_list = []

    if filter_project:
        for code in municipality_code_list:
            filter_query_list.append("properties/codegemeente eq '{}' and properties/project eq '{}'".format(code, filter_project))
    else:
        for code in municipality_code_list:
            filter_query_list.append("properties/codegemeente eq '{}'".format(code))

    filter_query = ' or '.join(filter_query_list)

    sensors = []
    result = requests.get("https://api-samenmeten.rivm.nl/v1.0/Things?$filter={query}".format(query=filter_query))

    while '@iot.nextLink' in result.json().keys():
        next_link = result.json()['@iot.nextLink']
        sensors += result.json()['value']
        result = requests.get(next_link)

    sensors += result.json()['value']
    return sensors

def get_sensor_location(sensor):
    # Request sensor location data
    location_link = sensor['Locations@iot.navigationLink']
    location_request = requests.get(location_link)

    # Extract sensor coordinates
    try:
        coordinates = location_request.json()['value'][0]['location']['coordinates']
    except IndexError:
        return None, None

    coordinates.reverse()

    return tuple(coordinates)

def get_all_sensor_data(sensor):
    # Initialize dictionary for row
    row_dict = {}

    # Sensor name
    row_dict['name'] = sensor['name']

    # Gemeentecode
    row_dict['codegemeente'] = sensor['properties']['codegemeente']

    # Location
    row_dict['latitude'], row_dict['longitude'] = get_sensor_location(sensor)

    # Add observations to row_dict
    for obs_type in ['temp', 'rh', 'pm25_kal', 'pm10_kal']:
        row_dict = update_observation_dict(row_dict, sensor, obs_type)
    # Append data to output list
    return row_dict

def write_timestamp(path, filename):
    # Write date and time to file to show when data was last updated
    current_date_and_time = str(datetime.datetime.now())
    with open(os.path.join(path, filename), 'w') as f:
        f.write(current_date_and_time + '\n')


if __name__ == '__main__':
    # Make an output folder called data if it does not exist yet
    output_dir = make_output_dir('data')

    # Provinces Groningen, Friesland and Drenthe
    municipality_code_list = get_province_municipality_codes([20,21,22])

    # Get information of all sensors
    sensors = get_sensors_in_municipalities(municipality_code_list, filter_project='Luftdaten')

    # Create empty dataframe with appropriate columns
    df = pd.DataFrame(columns=['name', 'codegemeente', 'latitude', 'longitude', 'date', 'temp', 'rh', 'pm25_kal', 'pm10_kal'])

    progress_bar = IncrementalBar('Downloading sensor data %(index)d of %(max)d', max=len(sensors), suffix='ETA: %(eta_td)s')
    for s in sensors:
        # Append sensor data to dataframe
        df = df.append(get_all_sensor_data(s), ignore_index=True)
        progress_bar.next()

    progress_bar.finish()

    # Write data to CSV file
    df.to_csv(os.path.join(output_dir, 'sensors.csv'), index=False)
    write_timestamp(output_dir, 'datetime.txt')
