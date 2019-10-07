from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import csv

# NOTE: requests-html does not work in a Jupyter environment

# create an HTML Session object
session = HTMLSession()
# Use the object above to connect to needed webpage
resp = session.get("https://coinfarm.online/position/position_realtime.asp")
# Run JavaScript code on webpage
resp.html.render(sleep=5)
soup = BeautifulSoup(resp.html.html, 'html.parser')

# Get short and long values
values_dict = {'long_val': soup.find('span', {'id':'t_long'}).text,
               'long_ratio': soup.find('span', {'id':'t_long2'}).text,
               'short_ratio': soup.find('span', {'id':'t_short2'}).text,
               'short_val': soup.find('span', {'id':'t_short'}).text}

# with open('data/Coinfarm/long_short_values.csv', 'w', newline='') as file:
#     writer = csv.DictWriter(file, fieldnames=['long_val', 'long_ratio', 'short_ratio', 'short_val'])
#     writer.writeheader()
#     writer.writerows(values_dict)

with open('data/Coinfarm/long_short_values.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in values_dict.items():
        writer.writerow([key, value])

# Get table data
td_tag = soup.body.center.find('table', {'style':"background:#253440;"},
                               recursive=False).find('td',{"style":"background:url('/public/bg_2.png') no-repeat ;"})
table_tag = td_tag.table.tbody.find_all('tr',recursive=False)[7]
table_long = table_tag.find('div', {'id':'vm_long'}).table.tbody.find_all('tr')
table_short = table_tag.find('div', {'id':'vm_short'}).table.tbody.find_all('tr')

# Scrape for header values in the table
headers = []
for i in range(1, len(table_long[0].find_all('td')) - 1):
    headers += [table_long[0].find_all('td')[i].text]

filename = ['long_table', 'short_table']
# Create a table, append rows to it and save to csv
for idx, table in enumerate([table_long, table_short]):
    row_list = []
    # Skip the 0th index iteration because it points to the headers
    for i in range(1, len(table)):
        long_dict = dict((headers[j], table[i].find_all('td')[j+1].text) for j in range(len(headers)))
        row_list.append(long_dict)
    table_df = pd.DataFrame(row_list, columns=headers)
    table_df.to_csv('data/Coinfarm/' + filename[idx] + '.csv', index=False)
