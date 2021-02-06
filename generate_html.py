import pandas as pd
import os
import math
from datetime import datetime
import folium
from jinja2 import Environment, FileSystemLoader

def timestamp():
    with open(os.path.join('data', 'datetime.txt')) as f:
        raw = f.readline()
        stripped = raw.split('.')[0]
        encoded = datetime.strptime(stripped, '%Y-%m-%d %H:%M:%S')
        return encoded.strftime('%d-%m-%Y %H:%M')

def mean_data(fix_eemsdelta=True):
    # Map province codes to sensors
    df = pd.read_csv(os.path.join('data', 'sensors.csv'))
    municipalities = pd.read_csv('gemeenten-alfabetisch-2021.csv')

    if fix_eemsdelta:
        eemsdelta_codes = [3, 24 ,10]
        municipalities = municipalities[~municipalities['Gemeentecode'].isin(eemsdelta_codes)]

    mun_prov_map = pd.Series(municipalities.Provinciecode.values, index=municipalities.Gemeentecode).to_dict()

    df['codeprovincie'] = df['codegemeente'].map(mun_prov_map)

    mun_code_name_map = pd.Series(municipalities.Gemeentenaam.values, index=municipalities.Gemeentecode).to_dict()
    prov_code_name_map = pd.Series(municipalities.Provincienaam.values, index=municipalities.Provinciecode).to_dict()

    province_codes = df['codeprovincie'].unique()

    province_data = []

    for prov_code in province_codes:
        mean_data = []

        for mun_code in mun_code_name_map.keys():
            if mun_prov_map[mun_code] == prov_code:
                mun_data = df[df['codegemeente'] == mun_code]
                
                mean_mun_data = {
                    'code': mun_code,
                    'name': mun_code_name_map[mun_code],
                    'pm10': mun_data['pm10_kal'].mean(),
                    'pm25': mun_data['pm25_kal'].mean(),
                    'temp': mun_data['temp'].mean(),
                    'rh': mun_data['rh'].mean(),
                    'n_sensors': len(mun_data),
                    'map': generate_municipality_map(mun_code)
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
                    elif k in ['pm10', 'pm25', 'rh']:
                        mean_mun_data[k] = round(mean_mun_data[k])
                    elif k in ['temp']:
                        mean_mun_data[k] = round(mean_mun_data[k], 1)

                mean_data.append(mean_mun_data)
        
        mean_data = sorted(mean_data, key=lambda k: k['name'])
        province_data.append({'name': prov_code_name_map[prov_code], 'municipalities': mean_data})

    province_data = sorted(province_data, key=lambda k: k['name'])
    return province_data

def generate_municipality_map(municipality_code):
    df = pd.read_csv(os.path.join('data', 'sensors.csv'))
    df = df[df['codegemeente'] == municipality_code]

    locations = []
    for _, row in df.iterrows():
        l = (row['latitude'], row['longitude'])
        locations.append(l)
    
    m = folium.Map()

    for l in locations:
        marker = folium.Marker(l)
        marker.add_to(m)

    sw = df[['latitude', 'longitude']].min().values.tolist()
    ne = df[['latitude', 'longitude']].max().values.tolist()

    m.fit_bounds([sw, ne])
    return m.get_root().render()

if __name__ == "__main__":
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')
    html_code = template.render(provinces=mean_data(), timestamp=timestamp())
    with open(os.path.join('static', 'index.html'), 'w') as f:
        f.write(html_code)
