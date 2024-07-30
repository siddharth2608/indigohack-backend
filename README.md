# TrackYourFlight
# Flight Status Notification System




The Flight Status Notification System is a web application designed to provide real-time flight status updates and notifications to passengers. Users can search for flights based on various criteria, subscribe to flight updates, and receive notifications about delays, cancellations, or gate changes. This system uses modern web technologies to deliver a seamless and interactive user experience.


## Features

- Real-Time Flight Search: Search flights by airport, date, airline, or flight number.
- Subscription Management: Subscribe or unsubscribe from flight status updates.
- Real-Time Notifications: Receive notifications via email for flight status changes (delays, cancellations, gate changes).
- User Authentication: Secure user login and registration.
- Dynamic UI: Responsive and modern UI with smooth transitions and animations.


## Tech
##### Frontend
- HTML, CSS, JavaScript
- jQuery
- Bootstrap (for styling and responsiveness)
##### Database
- PostgreSQL
##### Caching and Message Queuing
- Redis (for caching flight data)
- RabbitMQ (for sending email notifications)
##### Email Service
- SMTP (using Gmail for sending notifications)

##### Backend
- Python with Django
- Django REST Framework (for API endpoints)




## Installation

#### Prerequisites
- Python
- Django
- Redis
- RabbitMq


### Installation
##### 1. Clone the Repository

```sh
git clone https://github.com/siddharth2608/indigohack-backend.git
cd indigohack-backend
```

#### 2. Backend Setup
- Install python dependencies

```sh
pip install -r requirements.txt
```
- Run database migrations:
```sh
python manage.py migrate
```
#### 3.Run the Application
- Start the Django Server
```sh
python manage.py runserver
```
- Start RabbitMQ and Redis servers (make sure they are running).
- In another terminal do the following to run consumer script
```sh
cd flight_Service/
python email_worker.py
```

- In another terminal celery
```sh
celery -A TrackYourFlight_App worker -l INFO
```
- In another terminal run celery-beat
```sh
celery -A TrackYourFlight_App beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
#### 4. Testing
- Navigate to http://localhost:8000 in your web browser to access the application.


## Usage
- ##### Search Flights: Quickly find flights using our user-friendly search forms. Search by airport, date, airline, or flight number with real-time results.

- ##### Subscribe to Updates: Easily manage your flight subscriptions with a single click. Our system ensures you receive notifications only for the flights you're interested in.

- ##### Receive Notifications: Stay up-to-date with the latest changes in flight statuses, including delays, cancellations, and gate changes, delivered straight to your inbox..

#### Here is the Search Page
![airportnotify](https://github.com/user-attachments/assets/fd941572-a792-4959-b6ac-51888c0e2e0e)

#### Here is the example of notification mail
![notify2](https://github.com/user-attachments/assets/456bcce4-0bc4-4c71-a223-c45dbd63b977)


## Fun Fact
##### Did you know? The system’s email notification feature is powered by a custom-built email worker using RabbitMQ, which ensures that flight updates are delivered to you with minimal delay.

