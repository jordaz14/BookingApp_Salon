from flask import render_template, session
from functools import wraps
import datetime
from datetime import date

"""Time-related global variables and functionality to be access by booking-related routes"""

yearToday = date.today().year
monthToday = date.today().month
dayToday = date.today().day

weekdaysList = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

weekday = weekdaysList[datetime.datetime.today().weekday()]


def add_mins_to_time(timeval, mins_to_add):
    """Add minutes to datetime object"""
    dummy_date = datetime.date(1, 1, 1)
    full_datetime = datetime.datetime.combine(dummy_date, timeval)
    added_datetime = full_datetime + datetime.timedelta(minutes=mins_to_add)
    return added_datetime.time()


"""Log-In Helper"""


def login_required(f):
    """Decorate routes to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return render_template("login.html", error="You must be logged in to use this feature.")
        return f(*args, **kwargs)
    return decorated_function
