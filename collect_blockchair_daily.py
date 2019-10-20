import os
import gzip
import pandas as pd
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

r = requests.get('https://gz.blockchair.com/bitcoin/blocks/')
r.raise_for_status()

blockchair_bs = BeautifulSoup(r.text, 'html.parser')
file_url_list = blockchair_bs.pre.find_all('a')

# This scrapes for the last entry in the download page
file_url = file_url_list[-1].attrs['href']
download_url = 'https://gz.blockchair.com/bitcoin/blocks/' + file_url

# Download the file from `url` and save it locally under `filename`:
filename = "data/Blockchair/" + file_url[:-3]

with urlopen(download_url) as response, open(filename, 'wb') as file_out:
    file_out.write(gzip.decompress(response.read()))

# Read as csv before appending
new_filename = filename[:-3]+'csv'
blockchair_df = pd.read_csv(filename, sep='\t',
                            dtype={'version_bits': 'object', 'chainwork': 'object'}, index_col=['id'])

# Fix decimal place of certain columns
blockchair_df[['output_total', 'generation', 'reward']] = blockchair_df[['output_total', 'generation', 'reward']]*1e-8

# Append
blockchair_df.to_csv('data/Blockchair/blockchair.csv', mode='a', header=False)

# Delete file at 'filename'
try:
    os.remove(filename)
except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))
