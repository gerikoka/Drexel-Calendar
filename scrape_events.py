import requests
from bs4 import BeautifulSoup
import datetime
import os

def scrape_events():
    events = []
    url = 'https://drexel.edu/provost/policies-calendars/academic-calendars/quarters/'
    r = requests.get(url) 
    soup = BeautifulSoup(r.content, 'html5lib')

    for table in soup.find_all('div', class_='simple-accordion__body'): 
        body = table.find('tbody')

        for row in body.findAll('tr'):
            event = {}
            row_info = []
            
            for column in row.findAll('td'):
                non_strikethrough_text = ''.join([str(item) for item in column.contents if isinstance(item, str)])
                row_info.append(non_strikethrough_text.strip())

            if (len(row_info) == 0): # Skip empty rows
                continue

            if 'TBD' in row_info[1]:  # Skip rows with 'TBD' dates
                    continue

            event_date = row_info[1]
            event_title = row_info[2]

            try: 
                event['start'] = datetime.datetime.strptime(event_date, '%A, %B %d, %Y').strftime('%Y-%m-%d')
            except ValueError:
                print(f"Error parsing date: {event_date}")
                continue  # Skip rows with invalid date formats

            event['title'] = event_title
            event['id'] = 'scraped_event'
            events.append(event)

    return events
