import requests
import pandas as pd


r = requests.get('https://www.bitmex.com/api/v1/instrument?symbol=XBT&columns=timestamp%2C%20openInterest%2C%20openValue')
if r.status_code != 200:
    r.raise_for_status()

data = r.json()

instrument_df = pd.DataFrame(data)
instrument_df['openValue_BTC'] = instrument_df['openValue']/100000000
instrument_df.to_csv('data/Bitmex/OI_OV_XBT.csv', mode='a', header=False, index=False)

r = requests.get('https://www.bitmex.com/api/v1/instrument?symbol=ETH&columns=timestamp%2C%20openInterest%2C%20openValue')
if r.status_code != 200:
    r.raise_for_status()

data = r.json()

instrument_df = pd.DataFrame(data)
instrument_df.to_csv('data/Bitmex/OI_OV_ETH.csv', mode='a', header=False, index=False)