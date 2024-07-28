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
            flightElement.classList.add('flight');
            flightElement.innerHTML = `
                <p>Flight Number: ${flight.flight_number}</p>
                <p>Status: ${flight.status}</p>
                <p>Gate Number: ${flight.gate_number}</p>
                <p>Departure Time: ${new Date(flight.departure_time).toLocaleString()}</p>
            `;
            resultsContainer.appendChild(flightElement);
        });
    }
});
