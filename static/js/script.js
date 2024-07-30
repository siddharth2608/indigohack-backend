document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            tab.classList.add('active');
            document.getElementById(tab.dataset.tab).classList.add('active');
        });
    });

    // Fetch airlines and populate the dropdowns
    fetch('/flights/airlinesList')
    .then(response => response.json())
    .then(data => {
        const airlineSelect = document.getElementById('airline-name');
        data.airlines.forEach(item => {
            const option = document.createElement('option');
            option.value = item.airline;
            option.textContent = item.airline;
            airlineSelect.appendChild(option);
        });
    })
    .catch(error => console.error('Error fetching airlines:', error));

    // Event listeners for form submissions
    document.getElementById('search-by-airport-date').addEventListener('submit', event => {
        event.preventDefault();
        const departureAirport = event.target.departure_airport.value;
        const arrivalAirport = event.target.arrival_airport.value;
        const departureDate = event.target.departure_date.value;

        fetch(`/flights/searchflightdata/?departure_airport=${departureAirport}&arrival_airport=${arrivalAirport}&departure_date=${departureDate}`)
            .then(response => response.json())
            .then(data => {
                displayResults('results1', data);
            });
    });

    document.getElementById('search-by-airline-flight').addEventListener('submit', event => {
        event.preventDefault();
        const airlineName = event.target.airline_name.value;
        const flightNumber = event.target.flight_number.value;

        fetch(`/flights/searchflightdata/?airline_name=${airlineName}&flight_number=${flightNumber}`)
            .then(response => response.json())
            .then(data => {
                displayResults('results2', data);
            });
    });

    function displayResults(elementId, data) {
        const resultsContainer = document.getElementById(elementId);
        resultsContainer.innerHTML = '';

        if (data.length === 0) {
            resultsContainer.innerHTML = '<p>No results found.</p>';
            return;
        }

        data.forEach(flight => {
            const flightElement = document.createElement('div');
            flightElement.classList.add('flight-card');
            flightElement.innerHTML = `
                <div class="flight-card-header">
                    <h2>${flight.airline} - ${flight.flightnumber}</h2>
                    <p>${flight.departure} to ${flight.arrival}</p>
                </div>
                <div class="flight-card-body">
                    <p><strong>Gate Number:</strong> ${flight.gatenumber}</p>
                    <p><strong>Status:</strong> ${flight.status}</p>
                    <p><strong>Departure Date:</strong> ${flight.departuredate}</p>
                    <p><strong>Arrival Date:</strong> ${flight.arrivaldate}</p>
                </div>
                <div class="flight-card-footer">
            ${flight.userid ? 
                (flight.subscribe_status == '1' ?
                    `<button class="subscribe-button unsubscribe-button" data-flightnumber="${flight.flightnumber}" data-airline="${flight.airline}" data-action="0" onclick="subscribeToFlight(this)">Unsubscribe</button>` : 
                    `<button class="subscribe-button subscribe-button" data-flightnumber="${flight.flightnumber}" data-airline="${flight.airline}" data-action="1" onclick="subscribeToFlight(this)">Subscribe</button>`
                ) : 
                `<p class="no-subscription">Login to subscribe</p>`
            }
        </div>
            `;
            resultsContainer.appendChild(flightElement);
        });
    }
});

function subscribeToFlight(button) {
    const flightNumber = button.getAttribute('data-flightnumber');
    const airline = button.getAttribute('data-airline');
    const action = button.getAttribute('data-action');

    fetch('/flights/subscribe/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ flight_number: flightNumber, airline_name: airline, action: action })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            // Toggle button text and action
            if (action == 1) {
                button.textContent = 'Unsubscribe';
                button.setAttribute('data-action', '0');
            } else {
                button.textContent = 'Subscribe';
                button.setAttribute('data-action', '1');
            }
        } else {
            console.error('Error subscribing/unsubscribing:', data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}