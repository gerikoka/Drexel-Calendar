document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var holidays = [];

    // Function to calculate Martin Luther King Jr. Day
    function calculateMartinLutherKingJrDay(year) {
      // Calculate the third Monday in January
      var january = new Date(year, 0, 1);
      var dayOfWeek = january.getDay();
      var daysToAdd = dayOfWeek <= 1 ? 15 - dayOfWeek : 22 - dayOfWeek;
      var mlkDay = new Date(year, 0, daysToAdd + 1);
      return mlkDay;
    }

    // Function to calculate Presidents' Day
    function calculatePresidentsDay(year) {
      // Calculate the third Monday in February
      var february = new Date(year, 1, 1);
      var dayOfWeek = february.getDay();
      var daysToAdd = dayOfWeek <= 1 ? 15 - dayOfWeek : 22 - dayOfWeek;
      var presidentsDay = new Date(year, 1, daysToAdd + 1);
      return presidentsDay;
    }

    // Function to calculate Memorial Day
    function calculateMemorialDay(year) {
      // Start with May 31st and move backward to find the last Monday in May
      var may31 = new Date(year, 4, 31);
      while (may31.getDay() !== 1) {
        may31.setDate(may31.getDate() - 1);
      }
      return may31;
    }

    // Function to calculate Labor Day
    function calculateLaborDay(year) {
      // Find the first Monday in September
      var laborDay = new Date(year, 8, 1); // September is month 8 (0-based index)
      while (laborDay.getDay() !== 1) {
        laborDay.setDate(laborDay.getDate() + 1);
      }
      return laborDay;
    }

    // Function to calculate Columbus Day
    function calculateColumbusDay(year) {
      // Find the second Monday in October
      var columbusDay = new Date(year, 9, 1); // October is month 9 (0-based index)
      var count = 0;
      while (count < 2) {
        if (columbusDay.getDay() === 1) {
          count++;
        }
        if (count < 2) {
          columbusDay.setDate(columbusDay.getDate() + 1);
        }
      }
      return columbusDay;
    }

    // Function to calculate Thanksgiving Day
    function calculateThanksgivingDay(year) {
      // Find the fourth Thursday in November
      var thanksgivingDay = new Date(year, 10, 1); // November is month 10 (0-based index)
      var count = 0;
      while (count < 4) {
        if (thanksgivingDay.getDay() === 4) {
          count++;
        }
        if (count < 4) {
          thanksgivingDay.setDate(thanksgivingDay.getDate() + 1);
        }
      }
      return thanksgivingDay;
    }

    // Loop through years from 2020 to 2060
    for (var year = 2020; year <= 2060; year++) {
      // Add national holidays for the current year
      holidays.push(
        {
          title: "New Year's Day",
          start: year + '-01-01',
          allDay: true,
          color: 'red',
          backgroundColor: 'lightblue',
          borderColor: 'darkred',
          textColor: 'white'
        },
        {
          title: "Independence Day",
          start: year + '-07-04',
          allDay: true,
          color: 'blue',
          backgroundColor: 'lightblue',
          borderColor: 'darkblue',
          textColor: 'white'
        },
        {
          title: "Martin Luther King, Jr. Day",
          start: calculateMartinLutherKingJrDay(year),
          allDay: true,
          color: 'blue',
          backgroundColor: 'lightblue',
          borderColor: 'darkblue',
          textColor: 'white'
        },
        {
          title: "Presidents Day",
          start: calculatePresidentsDay(year),
          allDay: true,
          color: 'blue',
          backgroundColor: 'lightblue',
          borderColor: 'darkblue',
          textColor: 'white'
        },
        {
          title: "Memorial Day",
          start: calculateMemorialDay(year),
          allDay: true,
          color: 'blue',
          backgroundColor: 'lightblue',
          borderColor: 'darkblue',
          textColor: 'white'
        },
        {
          title: "Juneteenth",
          start: year + '-06-19',
          allDay: true,
          color: 'blue',
          backgroundColor: 'lightblue',
          borderColor: 'darkblue',
          textColor: 'white'
        },
        {
          title: "Labor Day",
          start: calculateLaborDay(year),
          allDay: true,
          color: 'blue',
          backgroundColor: 'lightblue',
          borderColor: 'darkblue',
          textColor: 'white'
        },
        {
          title: "Columbus Day",
          start: calculateColumbusDay(year),
          allDay: true,
          color: 'blue',
          backgroundColor: 'lightblue',
          borderColor: 'darkblue',
          textColor: 'white'
        },
        {
          title: "Veterans Day",
          start: year + '-11-11',
          allDay: true,
          color: 'blue',
          backgroundColor: 'lightblue',
          borderColor: 'darkblue',
          textColor: 'white'
        },
        {
          title: "Thanksgiving Day",
          start: calculateThanksgivingDay(year),
          allDay: true,
          color: 'blue',
          backgroundColor: 'lightblue',
          borderColor: 'darkblue',
          textColor: 'white'
        },
        {
          title: "Christmas Day",
          start: year + '-12-25',
          allDay: true,
          color: 'blue',
          backgroundColor: 'lightblue',
          borderColor: 'darkblue',
          textColor: 'white'
        }
      );
    }

    var holidayTitles = [
      "New Year's Day",
      "Independence Day",
      "Martin Luther King, Jr. Day",
      "Presidents Day",
      "Memorial Day",
      "Juneteenth",
      "Labor Day",
      "Columbus Day",
      "Veterans Day",
      "Thanksgiving Day",
      "Christmas Day"
    ];

    var calendar = new FullCalendar.Calendar(calendarEl, {
      navLinks: true,
      headerToolbar: {
        left: 'prev,next',
        center: 'title',
        right: 'multiMonthYear,dayGridMonth,timeGridWeek,timeGridDay' // user can switch between the two
      },
      initialView: 'timeGridWeek',

      eventSources: [
        {
          events: function (fetchInfo, successCallback, failureCallback) {
            // Fetch user-specific events
            fetch('/user_events')
              .then(response => response.json())
              .then(data => {
                successCallback(data);
              })
              .catch(error => {
                console.error('Error fetching user events:', error);
                failureCallback(error);
              });
          },
          color: '#E5B110', // Adjust the color according to your needs
          textColor: 'white'
        },
        {
          events: function (fetchInfo, successCallback, failureCallback) {
            // Fetch drexel-specific events
            fetch('/drexel_events')
              .then(response => response.json())
              .then(data => {
                successCallback(data);
              })
              .catch(error => {
                console.error('Error fetching user events:', error);
                failureCallback(error);
              });
          },
          color: '#E5B110', // Adjust the color according to your needs
          textColor: 'white'
        },
        holidays, // Add holidays as an event source
      ],

      eventContent: function(arg) {
        var eventEl = document.createElement('div');
        var isHoliday = holidayTitles.includes(arg.event.title);

        // Check if the event is a holiday, a Drexel event, or a user-created event
        if (isHoliday || arg.event.id == 'drexel') {
          // This is a holiday or a Drexel event, just display the title
          eventEl.appendChild(document.createTextNode(arg.event.title));
        } else {
          // Display the time and title for all views
          var eventTime = arg.event.start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
          var eventTitleWithTime = document.createElement('div');
          eventTitleWithTime.textContent = `${eventTime} - ${arg.event.title}`;
          eventTitleWithTime.style.fontSize = '10px';

          eventEl.appendChild(eventTitleWithTime);

          // Add delete button for week and day views
          if (calendar.view.type === 'timeGridWeek' || calendar.view.type === 'timeGridDay') {
            var deleteButton = document.createElement('button');
            deleteButton.innerHTML = '❌';
            deleteButton.classList.add('delete-event-button');

            eventEl.appendChild(deleteButton);

            deleteButton.addEventListener('click', function() {
              arg.event.remove(); // Remove the event from the calendar

              fetch(`/delete_event/${arg.event.id}`, {
                method: 'DELETE',
                headers: {
                  'Content-Type': 'application/json',
                },
              })
                .then(response => response.json())
                .then(data => {
                    console.log('Event deleted successfully:', data);
                })
                .catch(error => {
                  console.error('Error deleting event:', error);
                });
            });
          }
        }
        return { domNodes: [eventEl] };
      }
    });

    calendar.render();

    // Add Event button click event
  document.getElementById('addEventButton').addEventListener('click', function() {
    // Show the modal when the button is clicked
    document.getElementById('addEventModal').style.display = 'block';
  });

  // Save Event button click event
  document.getElementById('saveEventButton').addEventListener('click', function(event) {
    // Prevent the default form submission
    event.preventDefault();

    // Retrieve event information from the form
    var eventName = document.getElementById('eventName').value;
    var eventDate = document.getElementById('eventDate').value;
    var eventTime = document.getElementById('eventTime').value;

    // Add the new event to the calendar
    var newEvent = {
      title: eventName,
      start: new Date(eventDate + 'T' + eventTime), // Convert to Date object
      allDay: false,
      color: '#E5B110'
    };

    calendar.addEvent(newEvent);

    // Save the new event to the server
    fetch('/save_event', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newEvent),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Event saved successfully:', data);
      })
      .catch(error => {
        console.error('Error saving event:', error);
      });


    // Hide the modal after saving the event
    document.getElementById('addEventModal').style.display = 'none';
  });

  // Cancel button click event
  document.getElementById('cancelEventButton').addEventListener('click', function() {
    // Hide the modal when the cancel button is clicked
    document.getElementById('addEventModal').style.display = 'none';
  });

    // Show user greeting notification after 1 second
    setTimeout(function () {
      const notificationContainer = document.getElementById('notification-container');
      const continueButton = document.getElementById('continue-button');

      // Set the greeting message
      const greetingMessage = "Welcome to our Drexel-specific planner! Manage your coursework and exams with personalized student-life suggestions.";

      // Display the greeting notification
      notificationContainer.style.display = "block";
      notificationContainer.innerHTML = `<p>${greetingMessage}</p><button id="continue-button">Continue</button>`;

      // Hide the notification when the "Continue" button is clicked
      document.addEventListener("click", function (event) {
        if (event.target && event.target.id === "continue-button") {
          notificationContainer.style.display = "none";
        }
      });

    }, 1000);
  });