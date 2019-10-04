from requests_html import HTMLSession
from bs4 import BeautifulSoup
# create an HTML Session object
session = HTMLSession()
# Use the object above to connect to needed webpage
resp = session.get("https://coinfarm.online/position/position_realtime.asp")
# Run JavaScript code on webpage
resp.html.render(sleep=5)
soup = BeautifulSoup(resp.html.html, 'html.parser')

with open('coinfarm.txt', 'wb') as html_file:
    html_file.write(soup.get_text())