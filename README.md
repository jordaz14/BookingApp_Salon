# BOOKING APPLICATION

> Book your appointment with Corner Hair Salon today!

**OVERVIEW:**

I created a web app which allows users to create an account, search through the availability of different stylists, and register for an appointment; my inspiration for this project was to create a website which my mom (a hair salon owner) could use if she ever chose to take her business online.

**SKILLS:**

`JavaScript`, `Python (Flask)`, `HTML`, `CSS (Tailwind)`, `PostgreSQL`

**DESCRIPTION:**

The project is divided into 5 different sections: `Home`, `Services`, `Appointments`, `Gallery`, `Register`.

The `Home` page displays basic information about the business, featuring a banner with the business' slogan, text elements highlighting hours, contact, and location details, and the utilization of a Google Maps API to interactively display the business' location.

The `Services` page contains a menu list of all the available services provided by the salon; this information is templated through a backend database named 'services', thus allowing future functionality for an admin user to update and append services to this list with ease.

The `Gallery` page displays 6 photos which a user can click on to display a modal of the full image. To further enhance the functionality of this page, I'd like to incorporate a photo carousel once a photo is clicked, as well as an image upload feature for any admin users which log in.

The `Register` page allows a user to create an account or log-in if they already have one; the registration feature has both client and server-side form validation, as well as hashing of submitted passwords. To further enhance this page, I'd like to incorporate email verification once a user creates an account. Additionally, once a user logs in, it'd be beneficial for there to be a page which displays account information (e.g. name, email, password, upcoming appointments, etc.)

The `Appointment` page displays 3 stylists which a user can choose from to book an appointment. Depending on the stylist a user selects, they will then be displayed a list of available times (as well as the functionality to scroll through different dates); once a user clicks on a time, the appointment will be confirmed and no other user will be able to access this timeslot.
