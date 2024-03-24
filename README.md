# Drexel Calendar

## Documentation
fullcalendar: https://fullcalendar.io/

This repository contains code for a Drexel-specific planner. The planner is designed to help manage coursework and exams with personalized student-life suggestions. The planner includes features to manage national holidays, Drexel-specific events, user-created events, and courses.

## Features

- National Holidays: Displays national holidays such as New Year's Day, Independence Day, Martin Luther King, Jr. Day, Presidents Day, Memorial Day, Juneteenth, Labor Day, Columbus Day, Veterans Day, Thanksgiving Day, and Christmas Day on the calendar.
- Drexel-specific Events: Fetches Drexel-specific events and displays them on the calendar.
- User-created Events: Allows users to add and delete their events to the calendar.
- Courses: Allows users to add courses with their start dates, end dates, and meeting times. Automatically adds course events to the calendar based on meeting times.

## Usage

To use the planner, follow these steps:

1. Clone the repository to your local machine.
2. Move to the project's directory with the command **cd Drexel-Calendar**
3. The planner will load, displaying the calendar with national holidays, Drexel-specific events, and user-created events.
4. You can add courses by clicking the "Add Course" button and filling out the form. The course events will be automatically added to the calendar.
5. You can also add user-created events by clicking the "Add Event" button and filling out the form.
6. To remove a course or event, click the "Remove" button next to the respective item.
7. You can navigate between different views of the calendar using the navigation buttons at the top.

## How to Run app.py
Run the following commands to create a virtual environment on the **Drexel-Calendar** directory:
```bash
pip install virtualenv
python3 -m venv env
```
Next, activate your environment by running the following command:
```bash
source env/bin/activate
```
Then, install the necessary dependencies by running the following:
```bash
pip install -r requirements.txt
```
Lastly, run the following command to start the development server:
```bash
flask run
```
