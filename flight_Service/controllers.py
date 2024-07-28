from config import Config


class FlightController:

	def __init__(self):
		self.db_conn = Config.POSTGRESSQL_CONN


	def fetch_airlines_name(self):
		query='''select DISTINCT (airline) from flightdata'''
		result = self.db_conn.query_db(query)
		return result


	def get_flight_data(self,flight_search_filter):
		if(flight_search_filter["departure_airport"] and flight_search_filter["arrival_airport"] and flight_search_filter["departure_date"]):

			query = '''select * from flightdata where departure='{departure_airport}' and arrival='{arrival_airport}'
			and DATE_TRUNC('day', departuredate) ='{departure_date}'  '''.format(**flight_search_filter)

		elif (flight_search_filter["airline_name"] and flight_search_filter["flight_number"]):
			query = '''select * from flightdata where airline='{airline_name}' and flightnumber='{flight_number}'  '''.format(**flight_search_filter)

		result = self.db_conn.query_db(query)
		return result

