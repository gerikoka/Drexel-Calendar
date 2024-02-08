# Login functionality modified from https://www.geeksforgeeks.org/how-to-add-authentication-to-your-app-with-flask-login/

import requests
from bs4 import BeautifulSoup
import datetime
import os

from flask import Flask, request, redirect, render_template, send_from_directory, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user

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
            event['id'] = 'drexel'
            events.append(event)

    return events

app = Flask(__name__, static_folder='static')
 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "ENTER YOUR SECRET KEY"
db = SQLAlchemy()
 
login_manager = LoginManager()
login_manager.init_app(app)

class UserEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    start = db.Column(db.String(10), nullable=False)

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

        if user:
            if user.password == request.form.get("password"):
                login_user(user)
                return redirect(url_for("home"))
        else:
            flash("Invalid username or password. Please try again.", "error")

    return render_template("login.html")
 
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/user_events', methods=['GET'])
def get_user_events():
    if current_user.is_authenticated:
        user_id = current_user.id
        user_events = UserEvent.query.filter_by(user_id=user_id).all()
        events = [{'id': event.id, 'title': event.title, 'start': event.start} for event in user_events]
        return jsonify(events)
    else:
        return jsonify([])  # Return an empty list if the user is not authenticated

@app.route('/save_event', methods=['POST'])
def save_user_event():
    if current_user.is_authenticated:
        try:
            user_id = current_user.id
            event_data = request.get_json()

            # Save the event to the database
            new_event = UserEvent(
                title=event_data['title'],
                start=event_data['start'],
                user_id=user_id
            )
            db.session.add(new_event)
            db.session.commit()

            # Respond with the event_id
            return {'event_id': new_event.id}
        except Exception as e:
            print(f"Error saving event: {e}")
            return jsonify({'error': 'Error saving event'}), 500
    else:
        return jsonify({'error': 'User not authenticated'}), 401

@app.route('/delete_event/<int:event_id>', methods=['DELETE'])
def delete_user_event(event_id):
    if current_user.is_authenticated:
        user_id = current_user.id
        event_to_delete = UserEvent.query.filter_by(id=event_id, user_id=user_id).first()

        if event_to_delete:
            db.session.delete(event_to_delete)
            db.session.commit()
            return jsonify({'message': 'Event deleted successfully'})
        else:
            return jsonify({'error': 'Event not found'}), 404
    else:
        return jsonify({'error': 'User not authenticated'}), 401

@app.route('/drexel_events', methods=['GET'])
def get_drexel_events():
    events = scrape_events()
    return jsonify(events)

@app.route('/')
def home():  
    if current_user.is_authenticated:
        username = current_user.username
        user_events = current_user.events
        return render_template('index.html', username=username)
    else: 
        return render_template('index.html')

@app.route('/todo.html')
def todo():
    return render_template('todo.html')

@app.route('/tester')
def tester():
    events = scrape_events()
    return render_template('tester.html', events=events)

if __name__ == "__main__":
    app.run()