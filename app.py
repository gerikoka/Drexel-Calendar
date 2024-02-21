# Login functionality modified from https://www.geeksforgeeks.org/how-to-add-authentication-to-your-app-with-flask-login/
import os
from scrape_events import scrape_events
from admin import admin_bp
from flask import Flask, request, redirect, render_template, send_from_directory, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from flask_migrate import Migrate

app = Flask(__name__, static_folder='static')
 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "ENTER YOUR SECRET KEY"
db = SQLAlchemy()
migrate = Migrate(app, db)
 
login_manager = LoginManager()
login_manager.init_app(app)

class UserEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    start = db.Column(db.String(10), nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.String(10), nullable=False)
    end_date = db.Column(db.String(10))
    meeting_times = db.Column(db.String(10))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    is_done = db.Column(db.Boolean, default=False)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    events = db.relationship('UserEvent', backref='user', lazy=True)
    courses = db.relationship('Course', backref='user', lazy=True)
    tasks = db.relationship('Task', backref='user', lazy=True)
    is_admin = db.Column(db.Boolean, default=False)

db.init_app(app)
 
with app.app_context():
    db.create_all()

app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
 
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)
 
@app.route('/signup', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("signup.html")
 
@app.route("/login", methods=["GET", "POST"])
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

@app.route('/scraped_events', methods=['GET'])
def get_scraped_events():
    events = scrape_events()
    return jsonify(events)

@app.route('/courses', methods=['GET'])
def get_courses():
    if current_user.is_authenticated:
        user_id = current_user.id
        user_courses = Course.query.filter_by(user_id=user_id).all()
        courses = [{'id': course.id, 'name': course.name, 'start_date': course.start_date, 'end_date': course.end_date, 'meeting_times': course.meeting_times} for course in user_courses]
        return jsonify(courses)
    else:
        return jsonify([])  # Return an empty list if the user is not authenticated

@app.route('/save_course', methods=['POST'])
def save_course():
    if current_user.is_authenticated:
        try:
            user_id = current_user.id
            course_data = request.get_json()

            # Save the course to the database
            new_course = Course(
                name=course_data['name'],
                start_date=course_data['start_date'],
                end_date = course_data['end_date'],
                meeting_times = course_data['meeting_times'],
                user_id=user_id
            )
            db.session.add(new_course)
            db.session.commit()

            # Respond with the course_id
            return {'course_id': new_course.id}
        except Exception as e:
            print(f"Error saving course: {e}")
            return jsonify({'error': 'Error saving course'}), 500
    else:
        return jsonify({'error': 'User not authenticated'}), 401

@app.route('/delete_course/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    if current_user.is_authenticated:
        user_id = current_user.id
        course_to_delete = Course.query.filter_by(id=course_id, user_id=user_id).first()

        if course_to_delete:
            db.session.delete(course_to_delete)
            db.session.commit()
            return jsonify({'message': 'Course deleted successfully'})
        else:
            return jsonify({'error': 'Course not found'}), 404
    else:
        return jsonify({'error': 'User not authenticated'}), 401

@app.route('/tasks', methods=['GET'])
def get_tasks():
    if current_user.is_authenticated:
        user_id = current_user.id
        user_tasks = Task.query.filter_by(user_id=user_id).all()
        tasks = [{'id': task.id, 'title': task.title, 'is_done': task.is_done} for tasks in user_tasks]
        return jsonify(tasks)
    else:
        return jsonify([])  # Return an empty list if the user is not authenticated

@app.route('/add_task', methods=['POST'])
def add_task():
    if current_user.is_authenticated:
        try:
            user_id = current_user.id
            task_data = request.get_json()

            # Save the task to the database
            new_task = Task(
                title=task_data['title'],
                is_done=task_data['is_done'] == 'true',
                user_id=user_id
            )
            db.session.add(new_task)
            db.session.commit()

            # Respond with the task_id
            return {'task_id': new_task.id}
        except Exception as e:
            print(f"Error saving task: {e}")
            return jsonify({'error': 'Error saving task'}), 500
    else:
        return jsonify({'error': 'User not authenticated'}), 401

@app.route('/')
def home():  
    if current_user.is_authenticated:
        username = current_user.username
        user_events = current_user.events
        return render_template('index.html', username=username)
    else: 
        return render_template('index.html')

@app.route('/navbar')
def navbar():
    return render_template('navbar.html')

@app.route('/todo')
def todo():
    return render_template('todo.html')

@app.route('/tester')
def tester():
    return render_template('tester.html')

if __name__ == "__main__":
    app.run()