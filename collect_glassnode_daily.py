import pandas as pd
import requests


API_KEY = '022517a3-d79c-4510-9063-8d83780bb927'

variables = ['sopr', 'sopr_adjusted', 'cdd', 'average_dormancy', 'average_dormancy_supply_adjusted']
for var in variables:
    old_data_df = pd.read_csv('data/Glassnode/' + var + '.csv', usecols=['t'])
    final_timestamp = old_data_df.values[-1][0]
    # Filter from the time of 1 hour from last timestamp
    r = requests.get('https://api.glassnode.com/v1/metrics/indicators/'+ var + '?a=btc&s='+
                     str(final_timestamp+3600) + '&api_key=' + API_KEY)
    r.raise_for_status()
    json_file = r.json()
    if json_file:
        new_timestamp = json_file[0]['t']
        glassnode_df = pd.DataFrame(json_file)
        glassnode_df['Time'] = pd.to_datetime(glassnode_df['t'], unit='s')
        glassnode_df.to_csv('data/Glassnode/' + var + '.csv', mode='a', header=False, index=False)
