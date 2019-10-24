import requests
import pandas as pd
import os


def update_bitmex(params_dict={'symbol': 'XBTUSD', 'count': '100', 'reverse': 'false', 'start': '0'}):
    # Update data from timestamp of last entry in file
    api_call_url = 'https://www.bitmex.com/api/v1/funding?_format=csv'
    filepath = 'data/Bitmex/funding.csv'
    if os.path.isfile(filepath):
        pass
    else:
        filepath = '/opt/python/current/app/data/Bitmex/funding.csv'
    # Check if any parameters are applied
    if bool(params_dict):
        # Check for timestamp of last entry
        timestamp_df = pd.read_csv(filepath, usecols=['timestamp'])
        params_dict['startTime'] = timestamp_df.values[-1][0]
        params_dict['start'] = '1'
        for param in params_dict:
            api_call_url += '&' + param + '=' + params_dict[param]
        r = requests.get(api_call_url)
        if r.status_code != 200:
            r.raise_for_status()
        csv_list = r.text.split('\n')
        with open(filepath, 'a') as csv_file:
            # Append the data, but skip the headers
            for row in csv_list[1:]:
                csv_file.write('\n' + row)


update_bitmex()
