import requests
from bs4 import BeautifulSoup
import datetime

url = 'https://drexel.edu/provost/policies-calendars/academic-calendars/quarters/'
r = requests.get(url) 
  
soup = BeautifulSoup(r.content, 'html5lib')
table = soup.find('table', class_='DUVendors').find('tbody')
events = []

for row in table.findAll('tr'):
    event = {}
    rowInfo = []
    
    for column in row.findAll('td'):
        non_strikethrough_text = ''.join([str(item) for item in column.contents if isinstance(item, str)])
        rowInfo.append(non_strikethrough_text.strip())

    if 'TBD' in rowInfo[1]:  # Skip rows with 'TBD' dates
        continue

    event_date = rowInfo[1]
    event_title = rowInfo[2]

    try: 
        event['date'] = datetime.datetime.strptime(event_date, '%A, %B %d, %Y').strftime('%Y-%m-%d')
    except ValueError:
        print(f"Error parsing date: {event_date}")
        continue  # Skip rows with invalid date formats

    event['title'] = event_title
    events.append(event)

print(events[0])
