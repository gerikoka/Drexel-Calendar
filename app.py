# Login functionality modified from https://www.geeksforgeeks.org/how-to-add-authentication-to-your-app-with-flask-login/

import requests
from bs4 import BeautifulSoup
import datetime
import os

from flask import Flask, request, redirect, render_template, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user


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
 
# Tells flask-sqlalchemy what database to connect to
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
# Enter a secret key
app.config["SECRET_KEY"] = "ENTER YOUR SECRET KEY"
# Initialize flask-sqlalchemy extension
db = SQLAlchemy()
 
# LoginManager is needed for our application 
# to be able to log in and out users
login_manager = LoginManager()
login_manager.init_app(app)

class UserEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    start = db.Column(db.String(10), nullable=False)  # Adjust the data type according to your needs

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    events = db.relationship('UserEvent', backref='user', lazy=True)

db.init_app(app)
 
with app.app_context():
    db.create_all()
 
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)
 
@app.route('/sign_up.html', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("sign_up.html")
 
@app.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()
        print("username:", request.form.get("username"))
        if user.password == request.form.get("password"):
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html")
 
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def home():
    events = scrape_events()
    user_events = []
    
    if current_user.is_authenticated:
        username = current_user.username
        user_events = current_user.events

        if request.method == 'POST':
            print("Form data:", request.form)
            event_title = request.form.get('eventName')
            event_date = request.form.get('eventDate')

            # Additional debug prints
            print("Event Title:", event_title)
            print("Event Date:", event_date)

            # Additional validation and processing as needed
            new_event = UserEvent(title=event_title, start=event_date, user_id=current_user.id)
            db.session.add(new_event)
            db.session.commit()
        return render_template('index.html', events=events, username=username)
    else: 
        return render_template('index.html', events=events)

@app.route('/todo.html')
def todo():
    return render_template('todo.html')

@app.route('/tester')
def tester():
    events = scrape_events()
    return render_template('tester.html', events=events)

if __name__ == "__main__":
    app.run()