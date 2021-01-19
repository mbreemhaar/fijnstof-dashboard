import pandas as pd
import os
import math
from datetime import datetime
import requests

def timestamp():
    with open(os.path.join('data', 'datetime.txt')) as f:
        raw = f.readline()
        stripped = raw.split('.')[0]
        encoded = datetime.strptime(stripped, '%Y-%m-%d %H:%M:%S')
        return encoded.strftime('%d-%m-%Y %H:%M')

def mean_data():
    # Map province codes to sensors
    df = pd.read_csv(os.path.join('data', 'sensors.csv'))
    municipalities = pd.read_csv('gemeenten-alfabetisch-2021.csv')
    mun_prov_map = pd.Series(municipalities.Provinciecode.values, index=municipalities.Gemeentecode).to_dict()
    df['codeprovincie'] = df['codegemeente'].map(mun_prov_map)

    mun_code_name_map = pd.Series(municipalities.Gemeentenaam.values, index=municipalities.Gemeentecode).to_dict()
    prov_code_name_map = pd.Series(municipalities.Provincienaam.values, index=municipalities.Provinciecode).to_dict()

    province_codes = df['codeprovincie'].unique()
    municipality_codes = df['codegemeente'].unique()

    province_data = []

    for prov_code in province_codes:
        mean_data = []

        for mun_code in mun_code_name_map.keys():
            if mun_prov_map[mun_code] == prov_code:
                mun_data = df[df['codegemeente'] == mun_code]
                
                mean_mun_data = {
                    'name': mun_code_name_map[mun_code],
                    'pm10': round(mun_data['pm10_kal'].mean(), 2),
                    'pm25': round(mun_data['pm25_kal'].mean(), 2),
                    'temp': round(mun_data['temp'].mean(), 2),
                    'rh': round(mun_data['rh'].mean(), 2),
                    'n_sensors': len(mun_data)
                }

                if mean_mun_data['pm10'] >= 40 or mean_mun_data['pm25'] >= 25:
                    mean_mun_data['color'] = '#FF4A5F' # Red
                elif mean_mun_data['pm10'] >= 20 or mean_mun_data['pm25'] >= 10:
                    mean_mun_data['color'] = '#FFAB4A' # Orange
                else:
                    mean_mun_data['color'] = '#0BB5FF' # Blue

                for k in mean_mun_data.keys():
                    if type(mean_mun_data[k]) == float and math.isnan(mean_mun_data[k]):
                        mean_mun_data[k] = '--'
                        mean_mun_data['color'] = '#989898' # Light grey

                mean_data.append(mean_mun_data)
        
        province_data.append({'name': prov_code_name_map[prov_code], 'municipalities': mean_data})

    return province_data

def nearest_sensor_data(ip_address):
    api_data = requests.get('https://ipapi.co/{}/json/'.format(ip_address))

    user_city = api_data.json()['city']
    user_lat = api_data.json()['latitude']
    user_long = api_data.json()['longitude']
    
if __name__ == "__main__":
    print(nearest_sensor_data('82.73.164.165'))
