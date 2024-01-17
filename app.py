import requests
from bs4 import BeautifulSoup
import datetime
import os

from flask import Flask, render_template, send_from_directory

def scrape_events():
    url = 'https://drexel.edu/provost/policies-calendars/academic-calendars/quarters/'
    r = requests.get(url) 
    soup = BeautifulSoup(r.content, 'html5lib')
    table = soup.find('div', class_='simple-accordion__body').find('tbody')
    events = []

    for row in table.findAll('tr'):
        event = {}
        row_info = []
        
        for column in row.findAll('td'):
            non_strikethrough_text = ''.join([str(item) for item in column.contents if isinstance(item, str)])
            row_info.append(non_strikethrough_text.strip())

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
        events.append(event)

    return events

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    events = scrape_events()
    return render_template('index.html', events=events)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/index.html')
def homepage():
    events = scrape_events()
    return render_template('index.html', events=events)

@app.route('/tester.html')
def tester():
    events = scrape_events()
    return render_template('tester.html', events=events)


if __name__ == "__main__":
    app.run()