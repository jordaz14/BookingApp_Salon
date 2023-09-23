# Install modules
import psycopg2
from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import datetime
from datetime import date

# Modules from helpers.py
from helpers import weekdaysList, add_mins_to_time, yearToday, monthToday, dayToday, weekday, login_required

# Configure application
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Establish connection to database
conn = psycopg2.connect(
    host='localhost',
    dbname='salon',
    user='postgres',
    password='[PASSWORD]',
    port=5432
)

# Open cursor for database
db = conn.cursor()

"""APPLICATION ROUTING"""


@app.route("/")
def index():
    """Render homepage"""
    return render_template('index.html')


@app.route("/service")
def service():
    """Render list of services"""
    serviceDict = {}

    # Select all distinct services in database
    db.execute("SELECT DISTINCT service FROM services")
    rowsDistinct = db.fetchall()

    # For each distinct service, gather info regarding description & price of service
    for row in rowsDistinct:
        db.execute(
            "SELECT description, price FROM services WHERE service = %s", row)
        rowDetails = db.fetchall()
        serviceDict[row[0]] = rowDetails

    # Server-side templating to check output from serviceDict{}
    for key, value in reversed(serviceDict.items()):
        print(key)
        for i in range(0, len(value)):
            for j in range(2):
                print(value[i][j])

    return render_template('service.html', serviceDict=serviceDict, key=key, value=value, length=len(value))


@app.route("/appt")
def appt():
    """Render appointment page"""
    return render_template('appt.html')


@app.route("/gallery")
def gallery():
    """Render photo gallery"""
    return render_template('gallery.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a user"""
    if request.method == "POST":

        # Gather inputs from registration form
        fName = request.form.get("fname")
        lName = request.form.get("lname")
        email = request.form.get("email")
        pw = request.form.get("pw")
        confirmPw = request.form.get("cpw")

        # Server-side validation of invalid entries
        if (not fName or not lName or not email or not pw or not confirmPw) or (pw != confirmPw):
            return render_template('register.html', error="There was an error attempting to register your acccount. Please try again")

        # Hash password prior to database entry
        pw = generate_password_hash(pw)

        # Checks if user already exists in database, prompts user to try to logging in if so
        try:
            db.execute('INSERT INTO users (fname, lname, email, hashpw, confirmed) VALUES (%s, %s, %s, %s, %s)',
                       (fName, lName, email, pw, False))
            conn.commit()
        except:
            return render_template('register.html', error="You already have an email associated with this account. Try logging in.")

        return render_template('login.html')

    else:
        return render_template('register.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log-in a user"""
    # Clears existing user session info
    session.clear()

    if request.method == "POST":

        # Gather inputs from login form
        email = request.form.get("email")
        pw = request.form.get("pw")
        cpw = request.form.get("cpw")

        # Server-side validation of valid email imput / matching passwords
        if not email or (pw != cpw):
            return render_template('login.html', error="There was an error attempting to log in to your acccount. Please try again")

        emailTuple = (email,)
        db.execute("SELECT * FROM users WHERE email=%s", emailTuple)
        rows = db.fetchall()

        # Check if user exists and if so, if password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][4], pw):
            return render_template('login.html', error="There was an error attempting to log in to your acccount. Please try again")

        # Saves user email as user id
        session["user_id"] = rows[0][0]

        return redirect("/")

    if request.method == "GET":
        return render_template('login.html')


# Route for logout
@app.route("/logout")
def logout():
    """Log-out a user"""

    # Forget any user_id
    session.clear()

    # Redirect user to homepage
    return redirect("/")


@app.route("/calendar", methods=["GET", "POST"])
@login_required
def calendar():
    """Format and output employee availability for TODAY"""
    if request.method == "POST":
        # Format header of '[empName's] Calendar'
        # Global empID variable to be accessed /calendar/availability
        global empID
        empID = request.form.get("empID")
        db.execute("SELECT * FROM employees WHERE employee_id=%s", empID)
        rows = db.fetchall()
        empName = rows[0][1] + " " + rows[0][2]

        # Gather employee-related info regarding availability
        db.execute(
            "SELECT dayofweek, starttime, endtime FROM employeesavailable WHERE employee_id=%s AND dayofweek=%s", (empID, weekday))
        rows = db.fetchall()

        # Save start and end times to variables
        todayStart = rows[0][1]
        todayEnd = rows[0][2]
        todayInterval = datetime.time(0, 0, 0)

        empAvail = []
        empAvailFinal = []

        # Outputs sequence of times to empAvail list
        while todayInterval < todayEnd:
            if todayInterval == datetime.time(0, 0, 0):
                empAvail.append(todayStart)
                todayInterval = todayStart
            else:
                todayInterval = add_mins_to_time(todayInterval, 30)
                empAvail.append(todayInterval)

        # For each time in empAvail, check if that time already exists in booked appointments for today; if so, remove from list to display to user
        for times in empAvail:
            time = (times,)
            db.execute("SELECT EXISTS(SELECT * FROM bookedtimes WHERE appttime = %s AND emp_id = %s AND apptyear = %s AND apptmonth = %s AND apptday = %s)",
                       (time, empID, yearToday, monthToday, dayToday))
            rows = db.fetchall()
            if rows[0][0] == False:
                empAvailFinal.append(times)

        return render_template('calendar.html', empName=empName, empAvail=empAvailFinal, len=len(empAvailFinal))

    if request.method == "GET":
        return redirect('appt')


@app.route("/calendar/availability", methods=["GET", "POST"])
def calendarAvailable():
    """Format and output employee availability for EVERY OTHER DAY"""

    if request.method == "GET":
        return redirect('/')

    if request.method == "POST":
        # Declare global calInfo variable to hold times posted from JS, and to be accessed when users books appointment
        global calInfo
        calInfo = request.get_json()

        # Find employee availability for day POSTED through JS
        db.execute("SELECT dayofweek, starttime, endtime FROM employeesavailable WHERE employee_id=%s AND dayofweek=%s",
                   (empID, calInfo['weekday']))
        rows = db.fetchall()

        # See app.route /calendar for similar functionality
        todayStart = rows[0][1]
        todayEnd = rows[0][2]
        todayInterval = datetime.time(0, 0, 0)

        empAvail = []
        empAvailFinal = []
        empAvailJSON = []

        while todayInterval < todayEnd:
            if todayInterval == datetime.time(0, 0, 0):
                empAvail.append(todayStart)
                todayInterval = todayStart
            else:
                todayInterval = add_mins_to_time(todayInterval, 30)
                empAvail.append(todayInterval)

        for times in empAvail:
            time = (times,)
            db.execute("SELECT EXISTS(SELECT * FROM bookedtimes WHERE appttime = %s AND emp_id = %s AND apptyear = %s AND apptmonth = %s AND apptday = %s)",
                       (time, empID, calInfo['year'], calInfo['month']+1, calInfo['day']))
            rows = db.fetchall()
            if rows[0][0] == False:
                empAvailFinal.append(times)

        # Format list of times into appropriate format for return
        for times in empAvailFinal:
            times = times.strftime('%H:%M:%S')
            empAvailJSON.append(times)

        return empAvailJSON


@app.route("/calendar/bookappt", methods=["GET", "POST"])
def calendarBook():
    """Book user's appointment based off TODAY submission"""
    if request.method == "GET":
        return redirect('/')

    if request.method == "POST":

        # Cycles through register buttons to find correct bookBtn ID which submitted POST request
        i = 0
        while True:
            if ('bookBtn' + str(i)) in request.form:
                bookedTime = str(request.form.get('bookBtn'+str(i)))

                # Insert time into bookedtimes table, to be cross referenced when outputting available employee times
                db.execute("INSERT INTO bookedtimes (user_id, emp_id, apptyear, apptmonth, apptday, appttime, registranttype) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (session["user_id"], empID, yearToday, monthToday, dayToday, bookedTime, 'customer'))
                conn.commit()
                break
            else:
                i += 1

        return render_template('confirmation.html')


@app.route("/calendar/bookappt2", methods=["GET", "POST"])
def calendarBook2():
    """Book user's appointment based off EVERY OTHER DAY submission"""
    if request.method == "GET":
        return redirect('/')

    if request.method == "POST":
        bookedTime = request.form.get("register2")

        # Insert time into bookedtimes table, to be cross referenced when outputting available employee times
        db.execute("INSERT INTO bookedtimes (user_id, emp_id, apptyear, apptmonth, apptday, appttime, registranttype) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (session["user_id"], empID, calInfo['year'], calInfo['month']+1, calInfo['day'], bookedTime, 'customer'))
        conn.commit()

        return render_template('confirmation.html')
