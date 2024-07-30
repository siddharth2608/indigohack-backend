from config import Config
from auth_Service.controllers import AuthController
from TrackYourFlight_App.celery import app
from django.conf import settings
import requests

@app.task(name="send_notification")
def send_notification():
	print("inside send notification")
	redis_conn = Config.REDIS_CONN
	response = requests.get('http://127.0.0.1:8000/flights/getallflightsdata/')
	print("response")
	if response.status_code == 200:
		flight_data = response.json()
		for flight in flight_data:
			flight_key = f"flight:{flight['airline']}:{flight['flightnumber']}"
			cached_flight = redis_conn.hgetall(flight_key)
			if cached_flight:
				cached_flight = {k.decode('utf-8'): v.decode('utf-8') for k, v in cached_flight.items()}
				if (cached_flight.get('status') != flight['status'] and flight['status']=='Delayed'):
					push_notification_to_queue(flight,cached_flight,'Delayed')
					redis_client.hmset(flight_key, flight)
				elif ( cached_flight.get('status') != flight['status'] and flight['status']=='Cancelled'):
					push_notification_to_queue(flight,cached_flight,'Cancelled')
					redis_client.hmset(flight_key, flight)
				elif (cached_flight.get('gatenumber') != flight['gatenumber']):
					push_notification_to_queue(flight,cached_flight,'Gate')
					redis_client.hmset(flight_key, flight)
			else:
				print(flight_key)
				redis_conn.hmset(flight_key, flight)
				

def push_notification_to_queue(flight,oldflight,status):

	rabbit_conn = Config.RABBITMQ_CONN
	msg_data =  {
		'airline' : flight['airline'],
		'flight_number' : flight['flightnumber']
	}
	if(status=='Cancelled'):
		msg_data['msg'] = f"{flight['airline']} flight with Number {flight['flightnumber']} has been Cancelled due to some Circumstances"
	
	elif(status=='Delayed'):
		delay_by = calculate_delay(flight,oldflight)
		msg_data['msg'] = f"{flight['airline']} flight with Number {flight['flightnumber']} has been Delayed by {delay_by}. We are sorry for your inconvenience"
	
	elif(status=='Gate'):
		msg_data['msg'] = f"{flight['airline']} flight with Number {flight['flightnumber']} Gate Number has been changed. Please move toward Gate Number {flight['gatenumber']}"

	RABBITMQ_CONN.basic_publish(exchange='',
								routing_key='flight_notifications',
								body=json.dumps(msg_data))

def calculate_delay(flight,oldflight):
	scheduled_departure = datetime.strptime(oldflight['departuredate'], '%Y-%m-%dT%H:%M:%S')
	actual_departure = datetime.strptime(flight['departuredate'], '%Y-%m-%dT%H:%M:%S')
	delay_duration = actual_departure - scheduled_departure
	delay_hours = delay_duration.total_seconds() / 3600
	return delay_hours







