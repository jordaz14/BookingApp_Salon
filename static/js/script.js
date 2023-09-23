console.log(
  "'And now that you don't have to be perfect, you can be good.' -John Steinbeck"
);

/* ----- LAYOUT.HTML ----- */

// GOOGLE MAPS API
((g) => {
  var h,
    a,
    k,
    p = "The Google Maps JavaScript API",
    c = "google",
    l = "importLibrary",
    q = "__ib__",
    m = document,
    b = window;
  b = b[c] || (b[c] = {});
  var d = b.maps || (b.maps = {}),
    r = new Set(),
    e = new URLSearchParams(),
    u = () =>
      h ||
      (h = new Promise(async (f, n) => {
        await (a = m.createElement("script"));
        e.set("libraries", [...r] + "");
        for (k in g)
          e.set(
            k.replace(/[A-Z]/g, (t) => "_" + t[0].toLowerCase()),
            g[k]
          );
        e.set("callback", c + ".maps." + q);
        a.src = `https://maps.${c}apis.com/maps/api/js?` + e;
        d[q] = f;
        a.onerror = () => (h = n(Error(p + " could not load.")));
        a.nonce = m.querySelector("script[nonce]")?.nonce || "";
        m.head.append(a);
      }));
  d[l]
    ? console.warn(p + " only loads once. Ignoring:", g)
    : (d[l] = (f, ...n) => r.add(f) && u().then(() => d[l](f, ...n)));
})({
  key: "[API KEY]",
  v: "weekly",
});

let map;

// Edit location displayed on map
async function initMap() {
  const position = { lat: 31.9003075, lng: -106.4187642 };
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // Edit zoom and other style elements of the map
  if (document.getElementById("map")) {
    map = new Map(document.getElementById("map"), {
      zoom: 16,
      center: position,
      mapId: "DEMO_MAP_ID",
      mapTypeId: "satellite",
    });
  }

  const marker = new AdvancedMarkerElement({
    map: map,
    position: position,
    title: "[location input]",
  });
}

initMap();

// HAMBURGER MENU ICON
function hamburgerMenu() {
  let myLinks = document.getElementById("myLinks");
  if (myLinks.style.display === "block") {
    myLinks.style.display = "none";
  } else {
    myLinks.style.display = "block";
  }
}

// MODAL FUNCTIONALITY
// Modal to be retrieved later
let modal = document.getElementById("modal");

/* ----- CALENDAR.HTML ----- */

// DATE FUCTIONALITY
// Date (to edit) and current date (to use as reference)
let date = new Date();
const dateToday = new Date();

// List of weekdays and months to be indexed for formatting function
weekdayList = [
  "Sunday",
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
];

monthList = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

// Run function to initialize variables for today
dateFormatFunc();

function dateFormatFunc() {
  // Variables of global scope to be accessed later on
  (weekday = date.getDay()),
    (day = date.getDate()),
    (month = date.getMonth()),
    (year = date.getFullYear());

  // Format date info
  let dateFormat =
    monthList[month] +
    " " +
    day +
    ", " +
    year +
    " (" +
    weekdayList[weekday] +
    ")";

  // Assign date info to HTML element
  if (document.getElementById("today")) {
    document.getElementById("today").innerHTML = dateFormat;
  }
}

// Right-arrow button functionality
let datePlus1 = document.getElementById("datePlus1");
if (datePlus1) {
  datePlus1.addEventListener("click", () => Plus1());
  datePlus1.addEventListener("click", () => checkDate());
  datePlus1.addEventListener("click", () => sendDates());
}

// Left-arrow button functionality
let dateMinus1 = document.getElementById("dateMinus1");
if (dateMinus1) {
  dateMinus1.addEventListener("click", () => Minus1());
  dateMinus1.addEventListener("click", () => checkDate());
  dateMinus1.addEventListener("click", () => sendDates());
}

// Takes date and adds +/- days to input
function addDays(date, days) {
  let result = new Date(date);
  result.setDate(result.getDate() + days);
  return result;
}

// Adds day to current date
function Plus1() {
  date = addDays(date, 1);
  if (dateToday > date) {
    date = addDays(dateToday, 1);
    dateFormatFunc();
  } else {
    dateFormatFunc();
  }
}

// Removes day from current date
function Minus1() {
  date = addDays(date, -1);
  if (dateToday > date) {
    return;
  } else {
    dateFormatFunc();
  }
}

// Element which will hold list of available times as of today
let todayAvail = document.getElementById("todayAvail");

// Hides list of times once user clicks away from current date; candidly, this is a design flaw
function checkDate() {
  // Ensures user does not run function if they click left-button while on current date
  if (dateToday > date) {
    return;
  } else {
    // If new display does not equal today, hide listed times; otherwise, display
    if (
      dateToday.getDate() != date.getDate() ||
      dateToday.getMonth() != date.getMonth() ||
      dateToday.getFullYear() != date.getFullYear()
    ) {
      todayAvail.style.display = "None";
    } else {
      todayAvail.style.display = "Block";
    }
  }
}

// Set date data to backend
function sendDates() {
  // Clear existing output from page
  document.getElementById("forms").innerHTML = "";

  // Prevent user from sending input prior to today
  if (dateToday > date) {
    return;
  } else {
    // If display date on page != today, execute function
    if (
      dateToday.getDate() != date.getDate() ||
      dateToday.getMonth() != date.getMonth() ||
      dateToday.getFullYear() != date.getFullYear()
    ) {
      // Creates dict of calendar info to send to backend
      calInfo = {
        day: day,
        month: month,
        year: year,
        weekday: weekdayList[date.getDay()],
      };

      // Send calInfo to backend at /availability
      fetch("http://127.0.0.1:5000/calendar/availability", {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(calInfo),
        cache: "no-cache",
        headers: {
          "Content-Type": "application/json",
        },
      })
        // Wait for response from POST request to arrive
        .then((response) => response.json())
        // Convert response from Promise to Object
        .then((data) => (obj = data))
        // Run for loop to create form element for each time in object
        .then(() => {
          for (let i = 0; i < obj.length; i++) {
            console.log(obj[i]);

            // Create form element with action to /calendar/bookappt2
            var form = document.createElement("form");
            form.setAttribute("method", "post");
            form.setAttribute("action", "/calendar/bookappt2");

            // Create submit input with unique id for app.route /bookappt2 to register
            var s = document.createElement("input");
            s.setAttribute("type", "submit");
            s.setAttribute("id", i);
            s.setAttribute("name", "register2");
            s.setAttribute(
              "class",
              "bg-white rounded-md my-2 w-4/5 font-bold hover:bg-gray-300"
            );
            s.setAttribute("value", obj[i]);

            // Append submit button to form, append form to page
            form.append(s);
            document.getElementById("forms").appendChild(form);
          }
        });
    }
    // If display date on page = today, do not execute function
    else {
      return;
    }
  }
}

/* ----- GALLERY.HTML ----- */

let hairPhoto = document.getElementsByClassName("HairPhoto");
let hairModal = document.getElementsByClassName("HairMM");
let hairExit = document.getElementsByClassName("HairExit");

// Loops through every element gather through .getElementsbyClassname
for (let i = 0; i < hairPhoto.length; i++) {
  // Assigns onclick event listener to every hair photo
  hairPhoto[i].onclick = function () {
    modal.style.display = "block";
    hairModal[i].style.display = "block";
  };

  // Assigns onclick event listener to every exit button
  hairExit[i].onclick = function () {
    modal.style.display = "none";
    for (let j = 0; j < hairPhoto.length; j++) {
      hairModal[j].style.display = "none";
    }
  };
}

/* ----- REGISTER.HTML ----- */

// CLIENT-SIDE VALIDATION

// Assigns register button and checks matching passwords upon submission
let registerBtn = document.getElementById("Rbtn");

if (registerBtn) {
  registerBtn.addEventListener("click", matchPW);
}

function matchPW(event) {
  pw = document.getElementById("pw").value;
  confirmPw = document.getElementById("cpw").value;
  if (pw != confirmPw) {
    document.getElementById("CSerror").innerHTML =
      "Please enter matching passwords";
    event.preventDefault();
  }
}

// Checkbox to show passwords to allow user to visually confirm matching passwords
let checkPasswordCheck = document.getElementById("CPWcheck");
if (checkPasswordCheck) {
  checkPasswordCheck.addEventListener("click", showPW);
}

function showPW() {
  pw = document.getElementById("pw");
  confirmPw = document.getElementById("cpw");

  if (pw.type === "password") {
    pw.type = "text";
    confirmPw.type = "text";
  } else {
    pw.type = "password";
    confirmPw.type = "password";
  }
}

// Defines range of acceptable characters for user input in names; prompts the user on input if these characters aren't within range
let abcRange = /^[A-Za-z]+$/;

let fName = document.getElementById("fname");
if (fName) {
  fname.addEventListener("input", () => ABCvalidate(fName));
}

let lName = document.getElementById("lname");
if (lName) {
  lName.addEventListener("input", () => ABCvalidate(lName));
}

function ABCvalidate(name) {
  const errorElement = document.getElementById("CSerror");
  if (!abcRange.test(name.value)) {
    errorElement.innerHTML =
      "No spaces, numbers, or special characters allowed";
  } else {
    errorElement.innerHTML = "";
  }
}
