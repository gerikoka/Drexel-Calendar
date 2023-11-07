# this script gets a list of event dictionaries

import requests
from bs4 import BeautifulSoup

url = 'https://drexel.edu/provost/policies-calendars/academic-calendars/quarters/'
r = requests.get(url) 
  
soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib 
table = soup.find('table', attrs={'class': 'DUVendors'}).find('tbody')
# print(table.prettify())
events = []
for row in table.findAll('tr'):
    event = {}
    rowInfo = []
    for column in row:
        content = column.text
        if column.find('s') and column.find('s') != -1:
            content = content.strip(column.find('s').text)
        rowInfo.append(content)
    #print(rowInfo)
    event['date'] = rowInfo[3]
    event['name'] = rowInfo[5]
    events.append(event)
print(events)
