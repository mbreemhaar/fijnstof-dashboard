import requests
import pandas as pd
import sys
import os
import datetime

def get_observation(observation_type):
    datastream_request = requests.get(datastream_link + "?$filter=endswith(name, '{}')".format(observation_type))
    try:
        observation_link = datastream_request.json()['value'][0]['Observations@iot.navigationLink']
        observation_request = requests.get(observation_link + '?$top=1&$select=result,phenomenonTime')

        observation_result = observation_request.json()['value'][0]['result']
        observation_date = observation_request.json()['value'][0]['phenomenonTime']
        return observation_result, observation_date
    except:
        pass

# Create output directory at script location
script_dir = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(os.path.join(script_dir, 'data')):
    os.mkdir(os.path.join(script_dir, 'data'))

# Get all municipality codes in Groningen, Friesland and Drenthe
municipalities = pd.read_csv(os.path.join(script_dir, 'gemeenten-alfabetisch-2021.csv'))
filtered_municipalities = municipalities[municipalities.Provinciecode.isin([20,21,22])]
municipality_codes = filtered_municipalities['Gemeentecode']

# Generate query filter string for municipalities
filter_query_list = []
for code in municipality_codes:
    filter_query_list.append("properties/codegemeente eq '{}'".format(code))

filter_query = ' or '.join(filter_query_list)

# Retrieve Things filtered by municipality code
sensors = []
result = requests.get("https://api-samenmeten.rivm.nl/v1.0/Things?$filter={query}".format(query=filter_query))

while '@iot.nextLink' in result.json().keys():
    next_link = result.json()['@iot.nextLink']
    sensors += result.json()['value']
    result = requests.get(next_link)

sensors += result.json()['value']


df = pd.DataFrame(columns=['name', 'codegemeente', 'latitude', 'longitude', 'date', 'temp', 'rh', 'pm25_kal', 'pm10_kal'])

n_sensors = len(sensors)
progress_count = 0
for s in sensors:
    sys.stdout.write('\rRetrieving sensor data... ({}/{})'.format(progress_count + 1, n_sensors))

    # Initialize dictionary for row
    row_dict = {}

    # Sensor name
    row_dict['name'] = s['name']

    # Gemeentecode
    row_dict['codegemeente'] = s['properties']['codegemeente']

    # Request sensor location data
    location_link = s['Locations@iot.navigationLink']
    location_request = requests.get(location_link)

    # Extract sensor coordinates
    try:
        coordinates = location_request.json()['value'][0]['location']['coordinates']
        coordinates.reverse()
        row_dict['latitude'], row_dict['longitude'] = tuple(coordinates)
    except IndexError:
        continue

    # Get datastreams
    datastream_link = s['Datastreams@iot.navigationLink']

    # Get temperature
    temp_observation = get_observation('temp')
    if temp_observation:
        row_dict['temp'] = temp_observation[0]
        row_dict['date'] = temp_observation[1]

    rh_observation = get_observation('rh')
    if rh_observation:
        row_dict['rh'] = rh_observation[0]
        row_dict['date'] = rh_observation[1]

    pm25_kal_observation = get_observation('pm25_kal')
    if pm25_kal_observation:
        row_dict['pm25_kal'] = pm25_kal_observation[0]
        row_dict['date'] = pm25_kal_observation[1]
    
    pm10_kal_observation = get_observation('pm10_kal')
    if pm10_kal_observation:
        row_dict['pm10_kal'] = pm10_kal_observation[0]
        row_dict['date'] = pm10_kal_observation[1]
    
    # Append location data to output list
    df = df.append(row_dict, ignore_index=True)

    # Update progress counter
    progress_count += 1

sys.stdout.write('\nDone!\n')

# Write data to CSV file
df.to_csv(os.path.join(script_dir, 'data', 'sensors.csv'), index=False)

# Write date and time to file for test purposes
current_date_and_time = str(datetime.datetime.now())
with open(os.path.join(script_dir, 'data', 'datetime.txt'), 'w') as f:
    f.write(current_date_and_time + '\n')
