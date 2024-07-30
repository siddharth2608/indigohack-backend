from config import Config
from auth_Service.controllers import AuthController
from TrackYourFlight_App.celery import app
from django.conf import settings
import requests
import json
from datetime import datetime

@app.task(name="send_notification")
def send_notification():
	print("inside send notification")
	redis_conn = Config.REDIS_CONN
	response = requests.get('http://127.0.0.1:8000/flights/getallflightsdata/')
	print(response.status_code)
	if response.status_code == 200:
		flight_data = response.json()
		for flight in flight_data:
			flight_key = make_key_for_redis(flight['airline'], flight['flightnumber'])
			cached_flight = redis_conn.get(flight_key)
			if cached_flight:
				cached_flight = json.loads(cached_flight)
				
				if(flight['status']=='Delayed'):
					push_notification_to_queue(flight,cached_flight,'Delayed')
					redis_conn.setex(flight_key, 86400, json.dumps(flight))
				elif ( cached_flight.get('status') != flight['status'] and flight['status']=='Cancelled'):
					push_notification_to_queue(flight,cached_flight,'Cancelled')
					redis_conn.setex(flight_key, 86400, json.dumps(flight))
				elif (cached_flight.get('gatenumber') != flight['gatenumber']):
					push_notification_to_queue(flight,cached_flight,'Gate')
					redis_conn.setex(flight_key, 86400, json.dumps(flight))
				
			else:
				print(flight_key)
				redis_conn.setex(flight_key, 86400, json.dumps(flight))
				

def make_key_for_redis(airline,flightnumber):
	flight_key = airline.replace(" ", "").upper()
	return f"{flight_key}{flightnumber}"




def push_notification_to_queue(flight,oldflight,status):
	pushFlag = 'false'
	print("push t queu")
	rabbit_conn = Config.RABBITMQ_CONN
	msg_data =  {
		'airline' : flight['airline'],
		'flight_number' : flight['flightnumber']
	}
	if(status=='Cancelled'):
		msg_data['msg'] = f"{flight['airline']} flight with Number {flight['flightnumber']} has been Cancelled due to some Circumstances"
		pushFlag='true'
	
	elif(status=='Delayed'):
		if(oldflight['departuredate'] != flight['departuredate']):
			print(oldflight['departuredate'])
			print(flight['departuredate'])
			delay_by = calculate_delay(flight,oldflight)
			msg_data['msg'] = f"{flight['airline']} flight with Number {flight['flightnumber']} has been Delayed by {delay_by} hours. We are sorry for your inconvenience. New Timing for departure is {flight['departuredate']}"
			pushFlag='true'
	
	elif(status=='Gate'):
		msg_data['msg'] = f"{flight['airline']} flight with Number {flight['flightnumber']} Gate Number has been changed. Please move toward Gate Number {flight['gatenumber']}"
		pushFlag='true'

	if(pushFlag=='true'):
		rabbit_conn.basic_publish(exchange='',
									routing_key='flight_notifications',
									body=json.dumps(msg_data))

def calculate_delay(flight,oldflight):
	scheduled_departure = datetime.strptime(oldflight['departuredate'], '%Y-%m-%d %H:%M:%S')
	actual_departure = datetime.strptime(flight['departuredate'], '%Y-%m-%d %H:%M:%S')
	delay_duration = actual_departure - scheduled_departure
	delay_hours = int(delay_duration.total_seconds() / 3600)
	return delay_hours







