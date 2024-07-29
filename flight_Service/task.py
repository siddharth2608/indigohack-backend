from config import Config
from auth_Service.controllers import AuthController



@app.task(name="send_notification")
def send_notification():
	redis_conn = Config.REDIS_CONN
	response = requests.get('http://127.0.0.1:8000/flights/getallflightsdata/')
	if response.status_code == 200:
		flight_data = response.json()
		for flight in flight_data:
			flight_key = f"flight:{flight['airline']}:{flight['flightnumber']}"
			cached_flight = redis_conn.hgetall(flight_key)
			if cached_flight:
				cached_flight = {k.decode('utf-8'): v.decode('utf-8') for k, v in cached_flight.items()}
				if (
                    cached_flight.get('status') != flight['status'] or 
                    cached_flight.get('gatenumber') != flight['gatenumber']
                ):
	                send_notification(flight)
	                redis_client.hmset(flight_key, flight)
                
            else:
            	redis_conn.hmset(flight_key, flight)
            	

def send_notification(flight):
	users = AuthController().get_users_subscribed_to_notified(flight['airline'],flight['flightnumber'])
	